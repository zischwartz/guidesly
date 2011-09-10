import os
import random
import shutil
import zipfile
from datetime import datetime

from django.db import models
from django.db.models.base import ModelBase
from django.db.models.signals import post_save, post_init

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.conf import settings
from django.core.files.base import File, ContentFile
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from photologue.models import ImageModel

# attempt to load the django-tagging TagField from default location,
# otherwise we substitude a dummy TagField.
try:
    from tagging.fields import TagField
    tagfield_help_text = _('Separate tags with spaces, put quotes around multiple-word tags.')
except ImportError:
    class TagField(models.CharField):
        def __init__(self, **kwargs):
            default_kwargs = {'max_length': 255, 'blank': True}
            default_kwargs.update(kwargs)
            super(TagField, self).__init__(**default_kwargs)
        def get_internal_type(self):
            return 'CharField'
    tagfield_help_text = _('Django-tagging was not found, tags will be treated as plain text.')

# Path to default image
DEFAULT_IMAGE_PATH = getattr(settings, 'SAMPLE_IMAGE_PATH', os.path.join(os.path.dirname(__file__), 'res', 'default.jpg')) # os.path.join(settings.PROJECT_PATH, 'videologue', 'res', 'sample.jpg'

# Photologue image path relative to media root
VIDEOLOGUE_DIR = getattr(settings, 'VIDEOLOGUE_DIR', 'videologue')

# Look for user function to define file paths
VIDEOLOGUE_PATH = getattr(settings, 'VIDEOLOGUE_PATH', None)
if VIDEOLOGUE_PATH is not None:
    if callable(VIDEOLOGUE_PATH):
        get_storage_path = VIDEOLOGUE_PATH
    else:
        parts = VIDEOLOGUE_PATH.split('.')
        module_name = '.'.join(parts[:-1])
        module = __import__(module_name)
        get_storage_path = getattr(module, parts[-1])
else:
    def get_storage_path(instance, filename):
        return os.path.join(VIDEOLOGUE_DIR, 'videos', filename)

class Gallery(models.Model):
    date_added = models.DateTimeField(_('date published'), default=datetime.now)
    title = models.CharField(_('title'), max_length=100, unique=True)
    title_slug = models.SlugField(_('title slug'), unique=True,
                                  help_text=_('A "slug" is a unique URL-friendly title for an object.'))
    description = models.TextField(_('description'), blank=True)
    is_public = models.BooleanField(_('is public'), default=True,
                                    help_text=_('Public galleries will be displayed in the default views.'))
    videos = models.ManyToManyField('Video', related_name='galleries', verbose_name=_('videos'),
                                    null=True, blank=True)
    tags = TagField(help_text=tagfield_help_text, verbose_name=_('tags'))

    class Meta:
        ordering = ['-date_added']
        get_latest_by = 'date_added'
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()

    def get_absolute_url(self):
        return reverse('vl-gallery', args=[self.title_slug])

    def latest(self, limit=0, public=True):
        if limit == 0:
            limit = self.video_count()
        if public:
            return self.public()[:limit]
        else:
            return self.videos.filter(flv_video__isnull=False)[:limit]

    def sample(self, count=0, public=True):
        if count == 0 or count > self.video_count():
            count = self.video_count()
        if public:
            video_set = self.public()
        else:
            video_set = self.videos.filter(flv_video__isnull=False)
        return random.sample(video_set, count)

    def video_count(self, public=True):
        if public:
            return self.public().count()
        else:
            return self.videos.filter(flv_video__isnull=False).count()
    video_count.short_description = _('count')

    def public(self):
        return self.videos.filter(flv_video__isnull=False, is_public=True)


class GalleryUpload(models.Model):
    zip_file = models.FileField(_('images file (.zip)'), upload_to=VIDEOLOGUE_DIR+"/temp",
                                help_text=_('Select a .zip file of images to upload into a new Gallery.'))
    gallery = models.ForeignKey(Gallery, null=True, blank=True, help_text=_('Select a gallery to add these videos to. leave this empty to create a new gallery from the supplied title.'))
    title = models.CharField(_('title'), max_length=75, help_text=_('All videos in the gallery will be given a title made up of the gallery title + a sequential number.'))
    caption = models.TextField(_('caption'), blank=True, help_text=_('Caption will be added to all photos.'))
    description = models.TextField(_('description'), blank=True, help_text=_('A description of this Gallery.'))
    is_public = models.BooleanField(_('is public'), default=True, help_text=_('Uncheck this to make the uploaded gallery and included videos private.'))
    tags = models.CharField(max_length=255, blank=True, help_text=tagfield_help_text, verbose_name=_('tags'))

    class Meta:
        verbose_name = _('gallery upload')
        verbose_name_plural = _('gallery uploads')

    def save(self, *args, **kwargs):
        super(GalleryUpload, self).save(*args, **kwargs)
        gallery = self.process_zipfile()
        super(GalleryUpload, self).delete()
        return gallery

    def process_zipfile(self):
        if os.path.isfile(self.zip_file.path):
            # TODO: implement try-except here
            zip = zipfile.ZipFile(self.zip_file.path)
            bad_file = zip.testzip()
            if bad_file:
                raise Exception('"%s" in the .zip archive is corrupt.' % bad_file)
            count = 1
            if self.gallery:
                gallery = self.gallery
            else:
                gallery = Gallery.objects.create(title=self.title,
                                                 title_slug=slugify(self.title),
                                                 description=self.description,
                                                 is_public=self.is_public,
                                                 tags=self.tags)
            from cStringIO import StringIO
            for filename in zip.namelist():
                if filename.startswith('__'): # do not process meta files
                    continue
                data = zip.read(filename)
                if len(data):
                    while 1:
                        title = ' '.join([self.title, str(count)])
                        slug = slugify(title)
                        try:
                            p = Video.objects.get(title_slug=slug)
                        except Video.DoesNotExist:
                            video = Video(title=title,
                                          title_slug=slug,
                                          caption=self.caption,
                                          is_public=self.is_public,
                                          tags=self.tags)
                            video.original_video.save(filename, ContentFile(data), save=False)
                            video.save()
                            gallery.videos.add(video)
                            count = count + 1
                            break
                        count = count + 1
            zip.close()
            return gallery

""" Use signals to add videos to ConvertVideo for batch processing """

def set_original(sender, instance, **kwargs):

    try:
        instance.last_original_video = unicode(instance.original_video)
    except KeyError:
        instance.last_original_video = None

def add_convert(sender, instance, created, **kwargs):

    if instance.original_video != instance.last_original_video or created:

        ctype = ContentType.objects.get_for_model(sender)
        c = ConvertVideo.objects.create(content_type=ctype, object_id=instance.pk, started=False, error='')

""" Register signals to any base of VideoModel using a metaclass """

class VideoModelBase(ModelBase):

    def __new__(cls, name, bases, attrs):
        new = super(VideoModelBase, cls).__new__(cls, name, bases, attrs)
        if not new._meta.abstract:
            post_init.connect(set_original, sender=new)
            post_save.connect(add_convert, sender=new)
        return new

class VideoModel(ImageModel):

    __metaclass__ = VideoModelBase

    class Meta:
        abstract = True

    original_video = models.FileField(_('original video'), upload_to=get_storage_path)
    mp4_video = models.FileField(_('mp4 video'), null=True, upload_to=get_storage_path)
    ogv_video = models.FileField(_('ogv video'), null=True, upload_to=get_storage_path)
    flv_video = models.FileField(_('flv video'), null=True, upload_to=get_storage_path)

    def save(self, *args, **kwargs):
        if not self.image:
            self.image.save('default.jpg', File(open(DEFAULT_IMAGE_PATH)), save=False)
        super(VideoModel, self).save(*args, **kwargs)

class Video(VideoModel):

    title = models.CharField(_('title'), max_length=100, unique=True)
    title_slug = models.SlugField(_('slug'), unique=True,
                                  help_text=('A "slug" is a unique URL-friendly title for an object.'))
    caption = models.TextField(_('caption'), blank=True)
    date_added = models.DateTimeField(_('date added'), default=datetime.now, editable=False)
    is_public = models.BooleanField(_('is public'), default=True, help_text=_('Public photographs will be displayed in the default views.'))

    tags = TagField(help_text=tagfield_help_text, verbose_name=_('tags'))

    class Meta:
        ordering = ['-date_added']
        get_latest_by = 'date_added'
        verbose_name = _("video")
        verbose_name_plural = _("videos")

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()

    def save(self, *args, **kwargs):
        if self.title_slug is None:
            self.title_slug = slugify(self.title)
        super(Video, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('vl-video', args=[self.title_slug])

    def public_galleries(self):
        """Return the public galleries to which this photo belongs."""
        return self.galleries.filter(is_public=True)

    def get_previous_in_gallery(self, gallery):
        try:
            return self.get_previous_by_date_added(flv_video__isnull=False, galleries__exact=gallery)
        except Video.DoesNotExist:
            return None

    def get_next_in_gallery(self, gallery):
        try:
            return self.get_next_by_date_added(flv_video__isnull=False, galleries__exact=gallery)
        except Video.DoesNotExist:
            return None

class ConvertVideo(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    video = generic.GenericForeignKey('content_type', 'object_id')
    error = models.TextField(null=True, blank=True)
    started = models.BooleanField()

    def __unicode__(self):
        return unicode(self.video)

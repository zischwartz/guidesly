from django.db import models
import datetime 
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from django.conf import settings

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from imagekit.models import ImageModel
from django.db.models.signals import post_save, pre_save


SELEMENT_TYPE = (
	('image', 'Image'),
	('audio', 'Audio'),
	('video', 'Video'),
	('other', 'Other'),
)

class Image(ImageModel):
	original_image = models.ImageField(upload_to='uimages')
	class IKOptions:
		spec_module = 'fileupload.specs'
		cache_dir = 'userimagecache'
		image_field = 'original_image'
	def __unicode__(self):
		return self.original_image.name
		
class UserFile(models.Model):
	file = models.FileField(upload_to='userfiles', blank=True, null=True)
	slug = models.SlugField(max_length=150, blank=True)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	owner = models.ForeignKey(User, blank=True, null=True)
	type = models.CharField(blank=True, max_length=5, choices = SELEMENT_TYPE)
	image = models.ForeignKey(Image, blank=True, null=True)
	thumb_url = models.URLField(blank=True)
	medium_url = models.URLField(blank=True)
	display_url = models.URLField(blank=True)
	class Meta:
		ordering = ['-created']
	# content_type = models.ForeignKey(ContentType)


	def __unicode__(self):
		return self.file.name

	@property
	def url(self):
		# return (self.file.name) #removed string /media/ and changed slug to file
		return (settings.MEDIA_URL + self.file.name) #removed string /media/ and changed slug to file

	# def realsave(self, *args, **kwargs):		
	# 	if self.type == 'image':
	# 		self.thumb_url = self.image.thumbnail_image.url
	# 		self.medium_url = self.image.medium_image.url
	# 	if self.type == 'video':
	# 		self.thumb_url = "/static/img/video-icon.png"
	# 		self.medium_url = "/static/img/video-icon.png"
	# 	if self.type== 'audio':
	# 		self.thumb_url = "/static/img/audio-icon.png"
	# 		self.medium_url = "/static/img/audio-icon.png"
	# 	if self.type== 'other':
	# 		self.thumb_url = "/static/img/document-icon.png"
	# 		self.medium_url = "/static/img/document-icon.png"		
	# 	super(UserFile, self).save(*args, **kwargs)



def resize_images(sender, instance=None, **kwargs):
	if instance.type=='image':	
		instance.thumb_url = instance.image.thumbnail_image.url
		instance.medium_url = instance.image.medium_image.url
		instance.display_url = instance.image.display_image.url
	# if instance.type == 'video':
	# 	instance.thumb_url = "/static/img/video-icon.png"
	# 	instance.medium_url = "/static/img/video-icon.png"



pre_save.connect(resize_images, sender=UserFile)


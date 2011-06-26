from django.db import models
import datetime 
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from django.conf import settings

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

SELEMENT_TYPE = (
	('image', 'Image'),
	('audio', 'Audio'),
	('video', 'Video'),
	('other', 'Other'),
)

class UserFile(models.Model):

	file = models.FileField(upload_to='media/')
	slug = models.SlugField(max_length=150, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(User, blank=True, null=True)
	type = models.CharField(blank=True, max_length=5, choices = SELEMENT_TYPE)

	# content_type = models.ForeignKey(ContentType)
	# TODO add type of file here, maybe use contenttype fr

	def __unicode__(self):
		return self.file.name

	# @models.permalink
	@property
	def url(self):
		return (settings.MEDIA_URL +'media/'+ self.slug)
		# return ('upload-new', )

	def save(self, *args, **kwargs):
		# self.slug = slugify(self.file.name) #this takes out the period...
		# self.owner=			
		self.slug = self.file.name
		super(UserFile, self).save(*args, **kwargs)


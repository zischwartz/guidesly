from django.db import models
import datetime 
import tagging
from tagging.fields import TagField
from django.contrib.auth.models import User
from model_utils.managers import InheritanceManager
from django.template.defaultfilters import slugify
import jsonfield 

from fileupload.models import UserFile
# from learny.photologue.models import Photo


# from tastypie.resources import ModelResource
# from api.CardResource import CardResource

# Create your models here.
IELEMENT_TYPE = (
	('B', 'Just a Button'),
	('M', 'Multiple Choice'),
	('Y', 'Yes/No'),
	('V', 'Enter Value'),
	('N', 'Enter Numerical Value'),
	('S', 'Sensor'),
	('T', 'Timer'),
)

SELEMENT_TYPE = (
	('image', 'Image'),
	('audio', 'Audio'),
	('video', 'Video'),
	('other', 'Other'),
)

SVALUEINQUIRY_TYPE = (
	('L', 'Location'),
	('A', 'Accelerometer'),
	('T', 'Time'),
	('D', 'Date'),
)



class Guide (models.Model):
	title = models.CharField(max_length=500)
	slug = models.SlugField(unique=True, blank=True, max_length=250) #blank=true is silly but neccesary 
	description = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	is_linear = models.BooleanField(default=False) #if true, we should auto add next and back buttons
	enable_comments = models.BooleanField(default=True)
	text_slugs_for_cards = models.BooleanField(default=True)
	number_of_cards = models.IntegerField(default=1)
	tags = TagField()
	has_title_card = models.BooleanField(default=False)
	cards = models.ManyToManyField('Card', blank=True, null=True, related_name="cards_in_guide")
	card_order =jsonfield.JSONField(blank=True, null=True)

	def save(self, *args, **kwargs):
		self.slug= slugify(self.title)
		super(Guide, self).save(*args, **kwargs)
	
	def __unicode__(self):
		return self.title
		
	class Meta:
		ordering = ['-created']
		
	@models.permalink
	def get_absolute_url(self):
		return ('GuideDetailView', (), {'slug': self.slug })

class Card (models.Model):
	title = models.CharField(max_length=500, blank=True, null=True, default="") #maybe add default=""
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	slug = models.SlugField(blank=True)
	text = models.TextField(blank=True, null=True)
	guide= models.ForeignKey(Guide, null=True) #we'll use this as the default guide..., otherwise theres no absolute url
	brand_new = models.BooleanField(default=True)
	has_lots_of_text = models.BooleanField(default=False)
	tags = TagField()
	card_number = models.IntegerField(blank=True, null=True) #for default guide...
	representative_media = models.URLField(blank=True, null=True)
	
	def __unicode__(self):
		if self.title !="":
			return self.title
		else:
			return "Untitled Card #" + str(self.id)

	def save(self, *args, **kwargs):
		self.representative_media = self.rep_media
		if self.title:
			self.slug=slugify(self.title)
		else:
			self.slug = self.id # TODO this is hacky
		super(Card, self).save(*args, **kwargs)


	class Meta:
		ordering = ['created']
	
	@models.permalink
	def get_absolute_url(self):
		if self.slug:
			return ('CardDetailView', (), {'gslug': self.guide.slug, 'slug':self.slug })
		else:
			return ('CardDetailViewById', (), { 'id':self.id })

	@property
	def rep_media(self):
		primary =  self.mediaelement_set.filter(is_primary=True);
		if primary:
			return primary[0].file
			
		somemedia=self.mediaelement_set.all()
		if somemedia:
			return somemedia[0].file
		else:
			return None

	@property
	def resource_uri(self):
		r = CardResource() # cardresource is imported at the end of this file
		return r.get_resource_uri(self)



class MediaElement (models.Model):
	title = models.CharField(max_length=250, blank=True, null=True, default="")
	card = models.ForeignKey(Card)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	type = models.CharField(blank=True, max_length=5, choices = SELEMENT_TYPE)
	is_primary = models.BooleanField(default=True)
	is_background = models.BooleanField(default=False)
	autoplay = models.BooleanField(default=False)
	length_seconds = models.IntegerField(blank=True, null=True)
	length_minutes = models.IntegerField(blank=True, null=True)
	file = models.ForeignKey(UserFile)
	external_file = models.URLField(blank=True) #,verify_exists=True)

	#deprecate
	# @property
	# def file_url(self):
	# 	return self.file.url
	

class Action (models.Model):
	goto = models.ForeignKey(Card, blank=True, null=True)
	save_choice = models.BooleanField(default=False)
	play_static = models.ForeignKey(MediaElement, blank=True, null=True)
	def __unicode__(self):
		return "action-goto: %s" % self.goto


COND_TYPE = (
	('==', '=='),
	('>', 'is greater than'),
	('<', 'is less than'),
	('<=', 'is less than or equal to'),
	('>=', 'is greater than or equal to'),
	('!=', 'is not equal to'),
)


class ConditionalAction (models.Model):
	condition = models.CharField(max_length=2, choices = COND_TYPE, blank=True, null=True)
	text__match_answer = models.CharField(max_length=512, blank=True, null=True)
	b_number = models.FloatField( blank=True, null=True)
	goto_on_true = models.ForeignKey(Card, blank=True, null=True, related_name="goto_on_true")
	goto_on_false = models.ForeignKey(Card, blank=True, null=True, related_name="goto_on_false")
	save_choice = models.BooleanField(default=False)
	play_static = models.ForeignKey(MediaElement, blank=True, null=True)



class InputElement (models.Model):
	card = models.ForeignKey(Card)
	button_text = models.CharField(max_length=100)
	required = models.BooleanField(default=False)
	type = models.CharField(blank=True,  max_length=1, choices = IELEMENT_TYPE)
	default_goto = models.ForeignKey(Card, blank=True, null=True, related_name="+") #not using this so far
	default_action = models.OneToOneField(Action, blank=True, null=True)
	# default_action = models.ForeignKey(Action, blank=True, null=True)
	
	# def save(self, *args, **kwargs):
	# 	if not self.default_action:
	# 		someaction = Action()
	# 		someaction.save()
	# 		self.default_action=someaction
	# 	super(InputElement, self).save(*args, **kwargs)
	
	def el_template(self):
		return 'els/button.html'
		# return "<a class='ielement' href='%s'>%s</a>" % (self.default_action.goto.get_absolute_url(), self.button_text)
	def __unicode__(self):
		return self.button_text





# ********************************************************
# ***************         SIGH                ************
# ********************************************************

# class MultipleChoiceInquiry (InputElement):
# 	# choices = models.ForeignKey(MultipleChoices, blank=True, null=True) #deleted because we want multiple..duh
# 	show_choices = models.BooleanField(default=False)
# 	allow_multiple_selections = models.BooleanField(default=False)
# 	
# 	def el_template(self):
# 		return 'els/mc.html'
# 
# class MultipleChoice (models.Model):
# 	choice = models.CharField(max_length=250)
# 	action = models.ForeignKey(Action, blank=True, null=True)
# 	inquiry = models.ForeignKey(MultipleChoiceInquiry)
# 	def __unicode__(self):
# 		return self.choice
# 
# 
# #numerical
# class NValueInquiry (InputElement):
# 	min_value = models.FloatField(blank=True, null=True)
# 	max_value = models.FloatField(blank=True, null=True)
# 	increment_by = models.FloatField(blank=True, null=True)
# 	default_value = models.FloatField(blank=True, null=True)
# 	def el_template(self):
# 		return 'els/nvalue.html'
# 
# #text 
# class TValueInquiry (InputElement):
# 	default_value = models.CharField(max_length=500, blank=True, null=True,)
# 
# 	def el_template(self):
# 		return 'els/tvalue.html'
# 
# #sensor
# class SValueInquiry (InputElement):
# 	sensor_type = models.CharField(blank=True,  max_length=1, choices = SVALUEINQUIRY_TYPE)
# 	def el_template(self):
# 		return 'els/svalue.html'
# 	
# class Timer (InputElement):
# 	seconds = models.IntegerField(blank=True, null=True)
# 	minutes = models.IntegerField(blank=True, null=True)
# 	execute_action_when_done = models.BooleanField(default=True)




from api import CardResource

# USER PERMISSION PER OBJECT INSTANCE

# from object_permissions import register

# register(['permission'], Guide)
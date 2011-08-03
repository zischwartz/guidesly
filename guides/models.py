from django.db import models
import datetime 
import tagging
from tagging.fields import TagField
from django.contrib.auth.models import User
from model_utils.managers import InheritanceManager
from django.template.defaultfilters import slugify
import jsonfield 

from fileupload.models import UserFile

from log import getlogger
logger=getlogger()
logger.info("-------z--------")

# from learny.photologue.models import Photo


# from tastypie.resources import ModelResource
# from api.CardResource import CardResource



SELEMENT_TYPE = (
	('image', 'Image'),
	('audio', 'Audio'),
	('video', 'Video'),
	('other', 'Other'),
)

IELEMENT_TYPE = (
	('B', 'Just a Button'),
	('M', 'Multiple Choice'),
	('Y', 'Yes/No'),
	('V', 'Enter Value'),
	('N', 'Enter Numerical Value'),
	('S', 'Sensor'),
	('T', 'Timer'),
)



class Guide (models.Model):
	title = models.CharField(max_length=500)
	slug = models.SlugField(unique=True, blank=True, max_length=250) #blank=true is silly but neccesary 
	description = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	is_linear = models.BooleanField(default=True) #if true, we should auto add next and back buttons
	enable_comments = models.BooleanField(default=True)
	text_slugs_for_cards = models.BooleanField(default=True)
	tags = TagField()
	has_title_card = models.BooleanField(default=False)
	cards = models.ManyToManyField('Card', blank=True, null=True, related_name="cards_in_guide")
	card_order =jsonfield.JSONField(blank=True, null=True, default="[]") 

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
		
	def get_prev_card(self, card):
		prev_card_number = card.card_number -2 # 2 because the list card_order is zero based
		if prev_card_number >=0:
			return Card.objects.get(pk=(self.card_order[prev_card_number]))
		else: 
			return None

	def get_next_card(self, card):
		next_card_number = card.card_number  #no +1 because card_order is 0 based
		# logger.info(next_card_number)
		# logger.info(self.card_order)
		if not next_card_number >= len(self.card_order):
			return Card.objects.get(pk=(self.card_order[next_card_number]))
		else: 
			return None

class Card (models.Model):
	title = models.CharField(max_length=500, blank=True, null=True, default="") #maybe add default=""
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	slug = models.SlugField(blank=True, null=True)
	text = models.TextField(blank=True, null=True)
	guide= models.ForeignKey(Guide, null=True) #we'll use this as the default guide..., otherwise theres no absolute url
	brand_new = models.BooleanField(default=True)
	has_lots_of_text = models.BooleanField(default=False)
	tags = TagField()
	card_number = models.IntegerField(blank=True, null=True) #for default guide.  1 based (not 0)
	primary_media = models.ForeignKey('MediaElement', blank=True, null=True, related_name='primary_media', default="",  on_delete=models.SET_DEFAULT)
	is_floating_card = models.BooleanField(default=False)
	
	def __unicode__(self):
		if self.title !="":
			return self.title
		else:
			if not self.is_floating_card:
				return "Untitled Card #" + str(self.card_number)
			else: 
				return "Untitled Floating Card"
				
	def firstsave(self, *args, **kwargs):
		number_of_cards = len(self.guide.card_order)
		if not self.is_floating_card:
			self.card_number = number_of_cards +1
		super(Card, self).save(*args, **kwargs)
		if not self.is_floating_card:
			self.guide.card_order.append(self.id)
		self.guide.cards.add(self)
		self.guide.save()
		# logger.info("first save self.id")
		# logger.info(self.id)


	def save(self, *args, **kwargs):
		self.brand_new = False
		self.id=int(self.id) #quotes were messing up guide.card_order

		if self.title:
			self.slug=slugify(self.title)
		else:
			self.slug=None

		if self.is_floating_card:
			if self.id in self.guide.card_order:
				self.guide.card_order.remove(self.id)
				self.card_number = None
				self.guide.save()
		else: 
			if self.id in self.guide.card_order:
				pass
			else:
				number_of_cards = len(self.guide.card_order)
				self.card_number = number_of_cards +1
				self.guide.card_order.append(self.id)
				self.guide.save()
				# TODO this case is converting from a floating to a normal card. so where does it go? the end for now?
		super(Card, self).save(*args, **kwargs)

	
	def delete(self, *arg, **kwargs):
		if self.id in self.guide.card_order:
			self.guide.card_order.remove(self.id)
		super(Card, self).delete(*args, **kwargs)

	
	class Meta:
		ordering = ['created'] #switch to card_number
	
	@models.permalink
	def get_absolute_url(self):
		if not self.guide.text_slugs_for_cards:
			if card.is_floating_card:
				return ('CardDetailViewById', (), {'gslug': self.guide.slug, 'id':self.id })
			else:
				return ('CardDetailViewByNum', (), {'gslug': self.guide.slug, 'id':self.card_number})
		else:
			if self.slug:
				return ('CardDetailView', (), {'gslug': self.guide.slug, 'slug':self.slug })
			else:
				return ('CardDetailViewById', (), {'gslug': self.guide.slug, 'id':self.id })

	@property
	def resource_uri(self):
		r = CardResource() # cardresource is imported at the end of this file
		return r.get_resource_uri(self)



class MediaElement (models.Model):
	title = models.CharField(max_length=250, blank=True, null=True, default="")
	card = models.ForeignKey(Card)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	type = models.CharField(blank=True, max_length=5, choices = SELEMENT_TYPE)
	autoplay = models.BooleanField(default=False)
	length_seconds = models.IntegerField(blank=True, null=True)
	length_minutes = models.IntegerField(blank=True, null=True)
	file = models.ForeignKey(UserFile)
	external_file = models.URLField(blank=True) #,verify_exists=True)
	action_when_complete= models.OneToOneField('Action', blank=True, null=True)


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
	type = models.CharField(blank=True,  max_length=8, choices = IELEMENT_TYPE)
	default_goto = models.ForeignKey(Card, blank=True, null=True, related_name="+") #not using this so far
	default_action = models.OneToOneField(Action, blank=True, null=True)
	
	def el_template(self):
		return 'els/button.html'
		# return "<a class='ielement' href='%s'>%s</a>" % (self.default_action.goto.get_absolute_url(), self.button_text)
	def __unicode__(self):
		return self.button_text

from api import CardResource


	

# USER PERMISSION PER OBJECT INSTANCE

# from object_permissions import register

# register(['permission'], Guide)



# ********************************************************
# ***************         SIGH                ************
# ********************************************************
# 
# SVALUEINQUIRY_TYPE = (
# 	('L', 'Location'),
# 	('A', 'Accelerometer'),
# 	('T', 'Time'),
# 	('D', 'Date'),
# )


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




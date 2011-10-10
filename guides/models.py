from django.db import models
import datetime 
import tagging
from tagging.fields import TagField
from django.contrib.auth.models import User
# from model_utils.managers import InheritanceManager
from django.template.defaultfilters import slugify
from autoslug import AutoSlugField
from django.conf import settings

import jsonfield 

from fileupload.models import UserFile

from log import getlogger
logger=getlogger()
# logger.info("-------z--------")


SELEMENT_TYPE = (
	('image', 'Image'),
	('audio', 'Audio'),
	('video', 'Video'),
	('other', 'Other'),
)

IELEMENT_TYPE = (
	('button', 'Button'),
	('M', 'Multiple Choice'),
	('Y', 'Yes/No'),
	('V', 'Enter Value'),
	('N', 'Enter Numerical Value'),
	('S', 'Sensor'),
	('timer', 'Timer'),
	('place', 'Place'),
)

class Theme (models.Model):
	name = models.CharField(max_length=512)
	text = models.TextField(blank=True, null=True)
	owner = models.ForeignKey(User)
	is_public = models.BooleanField(default=True)
	def __unicode__(self):
		return self.name

class Guide (models.Model):
	title = models.CharField(max_length=500)
	slug = AutoSlugField(populate_from='title', unique=True)
	description = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	is_linear = models.BooleanField(default=True) #if true, we should auto add next and back buttons
	enable_comments = models.BooleanField(default=True)
	text_slugs_for_cards = models.BooleanField(default=True)
	tags = TagField()

	cards = models.ManyToManyField('Card', blank=True, null=True, related_name="cards_in_guide")
	card_order =jsonfield.JSONField(default="[]", blank=True) 
	floating_list =jsonfield.JSONField(default="[]", blank=True) 
	theme = models.ForeignKey(Theme, blank=True, null=True)
	owner = models.ForeignKey(User, blank=True, null=True)
	
	show_toc = models.BooleanField(default=False)
	first_card = models.ForeignKey('Card', blank=True, null=True, related_name="+")
	published = models.BooleanField(default=False)
	private = models.BooleanField(default=False)
	private_url = models.CharField(max_length=40, blank=True, null=True) #500 on server
	thumb = models.ForeignKey(UserFile, null=True, blank=True)
	
	submit_to_cat = models.BooleanField(default=True) #new to server
	accepted_to_cat = models.BooleanField(default=False) #new to server
	
	def save(self, *args, **kwargs):
		i=0
		thumb= self.thumb
		if self.is_linear:
			for c in self.card_order: #ugly
				i+=1
				card=Card.objects.get(pk=c)
				if i==1 and not self.show_toc:
					self.first_card = card #set first card to (you guessed it)			
				card.card_number = i
				card.is_floating_card= False
				card.saved_by_guide()
				if not thumb:
					images = card.mediaelement_set.filter(type='image')
					if len(images):
						if not images[0].external_file:
							self.thumb= images[0].file
					
		j=0
		for c in self.floating_list:
			j+=1
			card=Card.objects.get(pk=c)
			if not self.first_card and j==1 and not self.show_toc:
				self.first_card = card	
			card.is_floating_card= True
			card.card_number= 0
			card.saved_by_guide()
			if not thumb:
				images = card.mediaelement_set.filter(type='image')
				if len(images):
					if not images[0].external_file:
						self.thumb= images[0].file
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
		if not next_card_number >= len(self.card_order):
			return Card.objects.get(pk=(self.card_order[next_card_number]))
		else: 
			return None
			
	def get_guide_thumb(self):
		if self.thumb:
			return self.thumb.thumb_url




class Card (models.Model):
	title = models.CharField(max_length=500, blank=True, null=True, default="")
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True) #TODO ADD BACK IN
	slug = AutoSlugField(unique_with='guide__slug', populate_from=lambda instance: instance.title or 'card-'+str(instance.card_number) or 'sidecard')
	text = models.TextField(blank=True, null=True)
	guide= models.ForeignKey(Guide, null=True) #we'll use this as the default guide..., otherwise theres no absolute url
	tags = TagField()
	card_number = models.IntegerField(blank=True, null=True) #for default guide.  1 based (not 0)
	primary_media = models.ForeignKey('MediaElement', blank=True, null=True, related_name='primary_media', default=None,  on_delete=models.SET_DEFAULT)
	is_floating_card = models.BooleanField(default=False)
	theme = models.ForeignKey(Theme, blank=True, null=True)
	owner = models.ForeignKey(User, blank=True, null=True)
	autoplay = models.BooleanField(default=False)
	primary_is_bg = models.BooleanField(default=False)
	has_lots_of_text = models.BooleanField(default=False)
	show_next = models.BooleanField(default=True)
	show_prev = models.BooleanField(default=True)
	give_images_shadows = models.BooleanField(default=False)
	
	def __unicode__(self):
		if self.title !="":
			return self.title
		else:
			if not self.is_floating_card:
				return "Untitled Card #" + str(self.card_number)
			else: 
				return "Untitled Floating Card"
				

	@models.permalink # comment this out if using the hash...
	def get_absolute_url(self):
		# return '/s/' + self.guide.slug +"/#" + self.slug
		return ('CardInStackView', (), {'gslug': self.guide.slug, 'slug':self.slug })
				
	def firstsave(self, *args, **kwargs):
		self.owner= self.guide.owner
		if self.guide.is_linear:
			number_of_cards = len(self.guide.card_order)
			if not self.is_floating_card:
				self.card_number = number_of_cards
			super(Card, self).save(*args, **kwargs)
			if not self.is_floating_card:
				self.guide.card_order.append(self.id)
			else:
				self.guide.floating_list.append(self.id)
			self.guide.cards.add(self)
			self.guide.save()
		else:
			super(Card, self).save(*args, **kwargs)
			self.guide.floating_list.append(self.id)
			self.guide.cards.add(self)
			self.guide.save()



	def saved_by_guide(self, *args, **kwargs):
		super(Card, self).save(*args, **kwargs)
		
	#when the guide is saving the cards, it deals with the ordering.
	def save(self, *args, **kwargs):
		self.brand_new = False
		if self.title:
			if unicode.isalpha(self.title[0]):
				self.slug=slugify(self.title)
			else:
				self.slug = 'c'+ slugify(self.title) #later, we'll use the slug as the DOM id of the card
		else:
			self.slug=None
			
		if self.id:
			self.id=int(self.id) #quotes were messing up guide.card_order
		else: #if it doesn't have an id, just save the damn thing
			self.firstsave(*args, **kwargs)

		if self.is_floating_card:
			if self.id in self.guide.card_order: 
				# logger.info("switched from ordered to floating- saved")
				self.guide.card_order.remove(self.id)
				self.guide.floating_list.append(self.id)
				self.card_number = None
				self.guide.save()
			else:
				pass #it is floating, it was floating, it remains floating
		else: 
			if self.id in self.guide.card_order:
				pass
				# logger.info("saved an ordered card, it was already ordered")
			else:
				# logger.info("was unordered, now it is, adding it to order as last card")
				number_of_cards = len(self.guide.card_order)
				self.card_number = number_of_cards +1
				self.guide.card_order.append(self.id)
				self.guide.save()
				
		# If they didn't select a primary, give it one
		if not self.primary_media:
			images = self.mediaelement_set.filter(type='image')
			if len(images):
				self.primary_media = images[0]
			#defaults to video
			videos = self.mediaelement_set.filter(type='video')
			if len(videos):
				self.primary_media = videos[0]
				
		
		super(Card, self).save(*args, **kwargs)

	
	def delete(self, *args, **kwargs):
		if self.id in self.guide.card_order:
			self.guide.card_order.remove(self.id)
			self.guide.save()
		if self.id in self.guide.floating_list:
			self.guide.floating_list.remove(self.id)
			self.guide.save()
		super(Card, self).delete(*args, **kwargs)

	
	class Meta:
		ordering = ['is_floating_card','card_number'] 

	@property
	def resource_uri(self):
		r = CardResource() # cardresource is imported at the end of this file
		return r.get_resource_uri(self)
		
	def the_audio(self):
		return self.mediaelement_set.filter(type='audio')

	def the_video(self):
		return self.mediaelement_set.filter(type='video')
		
	def has_thumbs(self):
		count = len(self.mediaelement_set.filter(type='image'))
		count+= len(self.mediaelement_set.filter(type='video'))
		count+= len(self.mediaelement_set.filter(type='other'))
		if count > 1:
			return True
		else:
			return False
			
	def has_map(self):
		count = len(self.inputelement_set.filter(type='map'))
		if count:
			return True
		else:
			return False
		
	def cget_prev_card(self):
		prev_card_number = self.card_number -2 # 2 because the list card_order is zero based
		if prev_card_number >=0:
			return Card.objects.get(pk=(self.guide.card_order[prev_card_number]))
		else: 
			return None

	def cget_next_card(self):
		next_card_number = self.card_number  #no +1 because card_order is 0 based
		if not next_card_number >= len(self.guide.card_order):
			return Card.objects.get(pk=(self.guide.card_order[next_card_number]))
		else: 
			return None
			
	def get_thumb(self):
		if self.primary_media:
			if self.primary_media.type=='image':
				if self.primary_media.external_file:
					return self.primary_media.external_file
				else:
					return self.primary_media.file.thumb_url
			else:
				if self.primary_media.type=='video':
					return settings.STATIC_URL + 'img/video-icon.png'
				if self.primary_media.type=='audio':
					return SETTINGS.STATIC_URL + 'img/audio-icon.png'
				if self.primary_media.type=='other':
					return SETTINGS.STATIC_URL + 'img/other-icon.png'
					
		if self.has_map:
			return settings.STATIC_URL + 'img/map-thumb.png'
			
		return None
		
class CommentCard (Card):
	parent_card = models.ForeignKey(Card, related_name="child_comment_card", blank=True, null=True)
	parent_comment_card = models.ForeignKey("self", related_name="comments_child_comment_card", blank=True, null=True)

class MediaElement (models.Model):
	title = models.CharField(max_length=250, blank=True, null=True, default="")
	card = models.ForeignKey(Card)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	type = models.CharField(blank=True, max_length=5, choices = SELEMENT_TYPE)
	file = models.ForeignKey(UserFile, null=True)
	external_file = models.URLField(blank=True) #,verify_exists=True)
	action_when_complete= models.OneToOneField('Action', blank=True, null=True)
	def __unicode__(self):
		return "media-el: %s  (%s)" % (self.title, self.file)

class Action (models.Model):
	goto = models.ForeignKey(Card, blank=True, null=True)
	goto_guide = models.ForeignKey(Guide, blank=True, null=True)
	
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


class Condition (models.Model):
	condition = models.CharField(max_length=2, choices = COND_TYPE, blank=True, null=True)
	answer = models.CharField(max_length=512, blank=True, null=True)
	message = models.CharField(max_length=512, blank=True, null=True)
	action = models.OneToOneField(Action, blank=True, null=True)
	input = models.ForeignKey('InputElement')

class MapPointElement (models.Model):
	lat = models.FloatField(blank=True)
	long = models.FloatField(blank=True)
	button_text = models.CharField(max_length=150)
	sub_title = models.CharField(max_length=250, blank=True, null=True)
	manual_addy = models.CharField(max_length=250, blank=True)
	default_action = models.OneToOneField(Action, blank=True, null=True)
	card = models.ForeignKey(Card)

# class MapElement (models.Model):
# 	card = models.ForeignKey(Card)
# 	map_title = models.CharField(max_length=100)
# 	points = models.ManyToManyField(MapPointElement)
# 	type = models.CharField(max_length=100, default = 'map')

class InputElement (models.Model):
	card = models.ForeignKey(Card)
	big = models.BooleanField(default=False)
	button_text = models.CharField(max_length=250)
	sub_title = models.CharField(max_length=250, blank=True, null=True)
	type = models.CharField(blank=True,  max_length=8, choices = IELEMENT_TYPE)
	default_action = models.OneToOneField(Action, blank=True, null=True)
	big = models.BooleanField(default=False)
	
	# for timer
	seconds = models.IntegerField(default=0)
	minutes = models.IntegerField(default=0)
	execute_action_when_done = models.BooleanField(default=True)
	ding_when_done = models.BooleanField(default=False)
	auto_start = models.BooleanField(default=True) #or start on click
	
	# for text/ number input
	required = models.BooleanField(default=False)
	no_match_message =models.CharField(max_length=250, blank=True, null=True)
	should_save_answer = models.BooleanField(default=False)
	
	#for map
	lat = models.FloatField(blank=True, null=True)
	long = models.FloatField(blank=True, null=True)
	manual_addy = models.CharField(max_length=250, blank=True)
	
	def el_template(self):
		if self.type=="timer":
			return 'els/timer.html'
		if self.type == "button":
			return 'els/button.html'
		return 'els/button.html'
	def __unicode__(self):
		return self.button_text


from api import CardResource

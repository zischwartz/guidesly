from django.db import models
import datetime 


from model_utils.managers import InheritanceManager

# from learny.photologue.models import Photo


# Create your models here.
IELEMENT_TYPE = (
	('B', 'Just a Button'),
	('M', 'Multiple Choice'),
	('Y', 'Yes/No'),
	('V', 'Enter Value'),
	('N', 'Enter Numerical Value'),
	('S', 'Sensor'),
)

SELEMENT_TYPE = (
	('I', 'Image'),
	('A', 'Audio'),
	('V', 'Video'),
)

SVALUEINQUIRY_TYPE = (
	('L', 'Location'),
	('A', 'Accelerometer'),
	('T', 'Time'),
)



class Guide (models.Model):
	title = models.CharField(max_length=250)
	slug = models.SlugField(unique=True)
	description = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	is_linear = models.BooleanField(default=False) #if true, we should auto add next and back buttons
	enable_comments = models.BooleanField(default=True)
	text_slugs_for_slides = models.BooleanField(default=False)
	number_of_slides = models.IntegerField(default=0)
	
	def __unicode__(self):
		return self.title
		
	class Meta:
		ordering = ['-created']
		
	@models.permalink
	def get_absolute_url(self):
		return ('GuideDetailView', (), {'slug': self.slug })
	
	# def save(self, *args, **kwargs):
	# 	super(Guide, self).save(*args, **kwargs)
	# 	return self.id
		


class Slide (models.Model):
	title = models.CharField(max_length=250)
	slug = models.SlugField()
	text = models.TextField(blank=True, null=True)
	guide= models.ForeignKey(Guide, null=True)
	slide_number = models.IntegerField(blank=True, null=True)
	is_alt_slide = models.BooleanField(default=False) #if two slides have the same number, they're alt slides, meaning they're at the same level. sort of syntactic sugar...
	objects = InheritanceManager()
	def __unicode__(self):
		if self.title !='':
			return self.title
		else:
			return str(self.id)

	def save(self, *args, **kwargs):
		if not self.slide_number:
			n= self.guide.number_of_slides
			self.slide_number= n
			self.slug = n
			self.guide.number_of_slides = n+1
			self.guide.save()
		super(Slide, self).save(*args, **kwargs)


	class Meta:
		ordering = ['slide_number']
	
	@models.permalink
	def get_absolute_url(self):
		return ('SlideDetailView', (), {'gslug': self.guide.slug, 'slug':self.slug })



class StaticElement (models.Model):
	slide = models.ForeignKey(Slide)
	created = models.DateTimeField(auto_now_add=True)
	file = models.FileField(upload_to='media/%Y', blank=True) #the path obvs needs to include guide and slide
	title = models.CharField(max_length=250, blank=True, null=True)
	display_title = models.BooleanField(default=False) #if two slides have the same number, they're alt slides, meaning they're at the same level. sort of syntactic sugar...
	type = models.CharField(blank=True, max_length=1, choices = SELEMENT_TYPE)


class Action (models.Model):
	goto = models.ForeignKey(Slide, blank=True, null=True)
	save_choice = models.BooleanField(default=False)
	play_static = models.ForeignKey(StaticElement, blank=True, null=True)
	def __unicode__(self):
		return "action-goto: %s" % self.goto

class ConditionalAction (Action):
	condition = models.CharField(max_length=120)
	a_number = models.FloatField( blank=True, null=True)


#this base class is used for just a simple button, and is extended for the other types
class InteractiveElement (models.Model):
	slide = models.ForeignKey(Slide)
	button_text = models.CharField(max_length=100)
	required = models.BooleanField(default=False)
	type = models.CharField(blank=True,  max_length=1, choices = IELEMENT_TYPE)
	default_action = models.ForeignKey(Action, blank=True, null=True)
	text = models.TextField(blank=True, null=True)
	objects = InheritanceManager()
		
	def el_template(self):
		return 'els/button.html'
		# return "<a class='ielement' href='%s'>%s</a>" % (self.default_action.goto.get_absolute_url(), self.button_text)
	def __unicode__(self):
		return self.button_text


class MultipleChoiceInquiry (InteractiveElement):
	# choices = models.ForeignKey(MultipleChoices, blank=True, null=True) #deleted because we want multiple..duh
	show_choices = models.BooleanField(default=False)
	allow_multiple_selections = models.BooleanField(default=False)
	
	def el_template(self):
		return 'els/mc.html'

class MultipleChoice (models.Model):
	choice = models.CharField(max_length=250)
	action = models.ForeignKey(Action, blank=True, null=True)
	inquiry = models.ForeignKey(MultipleChoiceInquiry)
	def __unicode__(self):
		return self.choice

class YNInquiry (InteractiveElement):
	yes_action = models.ForeignKey(Action, blank=True, null=True, related_name='yn_inquiry_yes')
	no_action = models.ForeignKey(Action, blank=True, null=True, related_name='yn_inquiry_no')
	
	def el_template(self):
		return 'els/yn.html'

#numerical
class NValueInquiry (InteractiveElement):
	min_value = models.FloatField(blank=True, null=True)
	max_value = models.FloatField(blank=True, null=True)
	increment_by = models.FloatField(blank=True, null=True)
	default_value = models.FloatField(blank=True, null=True)
	def el_template(self):
		return 'els/nvalue.html'

#text 
class TValueInquiry (InteractiveElement):
	default_value = models.CharField(max_length=500, blank=True, null=True,)

	def el_template(self):
		return 'els/tvalue.html'

#sensor
class SValueInquiry (InteractiveElement):
	sensor_type = models.CharField(blank=True,  max_length=1, choices = SVALUEINQUIRY_TYPE)
	def el_template(self):
		return 'els/svalue.html'
	

class Timer (InteractiveElement):
	seconds = models.IntegerField(blank=True, null=True)
	minutes = models.IntegerField(blank=True, null=True)
	execute_action_when_done = models.BooleanField(default=True)

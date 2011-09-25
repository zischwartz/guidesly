from django.forms import ModelForm
from django import forms
from models import *
from django.forms.widgets import *
# from log import *
from tagging.forms import TagField
from tagging_autocomplete.widgets import TagAutocomplete

class GuideForm(ModelForm):
	# tags = TagField(widget=TagAutocomplete())
	class Meta:
		model=Guide
		fields = ('title', 'description', 'tags', 'enable_comments')#, 'first_card' )
		
		widgets = {
			'slug': HiddenInput,
			'number_of_cards': HiddenInput,
			}	

class PublishForm(ModelForm):
	class Meta:
		model=Guide
		fields = ('private', 'submit_to_cat', 'published' )
				
class CardForm(ModelForm):
	class Meta:
		model=Card

class StaticElementForm(ModelForm):
	class Meta:
		model=MediaElement
		widgets = {
			'card': HiddenInput,
			'type': HiddenInput,
			'file': HiddenInput,
			'title': TextInput(attrs={'placeholder': 'Title (optional)'})

			}


# this, at it's base, is a simple button
class InteractiveElementForm(ModelForm):
	class Meta:
		model=InputElement
		widgets = {
			'card': HiddenInput,
			'type': HiddenInput,
			}

# from log import *
# logger=getlogger()		
# logger.debug('-----------------------------------------------------------------------------------------------------------------')
# logger.debug(ModelForm.__subclasses__())

# model_form_dictionary={}
# for x in ModelForm.__subclasses__():
# 	model_form_dictionary[x._meta.model]= x



# logger.debug(moforms)

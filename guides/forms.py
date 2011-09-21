from django.forms import ModelForm
from django import forms
from models import *
from django.forms.widgets import *
# from log import *

class GuideForm(ModelForm):
	class Meta:
		model=Guide
		widgets = {
			'slug': HiddenInput,
			'number_of_cards': HiddenInput,
			}	

				
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

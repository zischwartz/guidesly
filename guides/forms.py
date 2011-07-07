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
		model=StaticElement
		widgets = {
			'card': HiddenInput,
			'type': HiddenInput,
			'file': HiddenInput,
			'title': TextInput(attrs={'placeholder': 'Title (optional)'})

			}




# class ImageSelect(forms.Select): 
# 	def render(self, name, value, attrs=None):
# 		# value = self._format_value(value)
# 		# return super(TimeInput, self).render(name, value, attrs)
# 		return 'x' + value

# 
# class ImageElementForm(ModelForm):
# 	# file = forms.ModelChoiceField()
# 	
# 	class Meta:
# 		model=ImageElement
# 		widgets = {
# 			'card': HiddenInput,
# 			'type': HiddenInput,
# 			'file': HiddenInput,
# 			'display_title': HiddenInput,
# 			'title': TextInput(attrs={'placeholder': 'Title (optional)'})
# 			}
# 
# class AudioElementForm(ModelForm):
# 	class Meta:
# 		model=AudioElement
# 		widgets = {
# 			'card': HiddenInput,
# 			'type': HiddenInput,
# 			}
# 
# 
# class VideoElementForm(ModelForm):
# 	class Meta:
# 		model=VideoElement
# 		widgets = {
# 			'card': HiddenInput,
# 			'type': HiddenInput,
# 			}



# this, at it's base, is a simple button
class InteractiveElementForm(ModelForm):
	class Meta:
		model=InteractiveElement
		widgets = {
			'card': HiddenInput,
			'type': HiddenInput,
			}

# from log import *
# logger=getlogger()		
# logger.debug('-----------------------------------------------------------------------------------------------------------------')
# logger.debug(ModelForm.__subclasses__())

model_form_dictionary={}
for x in ModelForm.__subclasses__():
	model_form_dictionary[x._meta.model]= x



# logger.debug(moforms)

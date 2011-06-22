from django.forms import ModelForm
from models import *
from django.forms.widgets import *
from log import *

class GuideForm(ModelForm):
	class Meta:
		model=Guide
		widgets = {
			'slug': HiddenInput,
			'number_of_slides': HiddenInput,

			}		
class SlideForm(ModelForm):
	class Meta:
		model=Slide

# class StaticElementForm(ModelForm):
# 	class Meta:
# 		model=StaticElement
# 		widgets = {
# 			'slide': HiddenInput,
# 			'type': HiddenInput,
# 			}

class ImageElementForm(ModelForm):
	class Meta:
		model=ImageElement
		widgets = {
			'slide': HiddenInput,
			'type': HiddenInput,

			}

class AudioElementForm(ModelForm):
	class Meta:
		model=AudioElement
		widgets = {
			'slide': HiddenInput,
			'type': HiddenInput,
			}


class VideoElementForm(ModelForm):
	class Meta:
		model=VideoElement
		widgets = {
			'slide': HiddenInput,
			'type': HiddenInput,
			}



# this, at it's base, is a simple button
class InteractiveElementForm(ModelForm):
	class Meta:
		model=InteractiveElement
		widgets = {
			'slide': HiddenInput,
			'type': HiddenInput,
			}


# logger=getlogger()		
# logger.debug('-----------------------------------------------------------------------------------------------------------------')
# logger.debug(ModelForm.__subclasses__())

model_form_dictionary={}
for x in ModelForm.__subclasses__():
	model_form_dictionary[x._meta.model]= x



# logger.debug(moforms)

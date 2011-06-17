from django.forms import ModelForm
from models import *
from django.forms.widgets import *


class GuideForm(ModelForm):
	class Meta:
		model=Guide
		
class SlideForm(ModelForm):
	class Meta:
		model=Slide

class StaticElementForm(ModelForm):
	class Meta:
		model=StaticElement
		widgets = {
			'slide': HiddenInput}

# this, at it's base, is a simple button
class InteractiveElementForm(ModelForm):
	class Meta:
		model=InteractiveElement
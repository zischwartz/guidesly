from django.forms import ModelForm
from models import *

class CreateGuideForm(ModelForm):
	class Meta:
		model=Guide
		
class CreateSlideForm(ModelForm):
	class Meta:
		model=Slide

class CreateStaticElementForm(ModelForm):
	class Meta:
		model=StaticElement
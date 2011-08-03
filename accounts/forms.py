from django.db import models
from django.forms import ModelForm 

from django.conf import settings
from django import forms


class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
      

from tastypie.resources import ModelResource

from guides.models import *
from tastypie import fields
from django.contrib.auth.models import User


class UserResource(ModelResource):
	class Meta:
		queryset= User.objects.all()
		excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
		allowed_methods = ['get']

		
class SlideResource(ModelResource):
	staticelements = fields.ToManyField('api.StaticElementResource', 'staticelement_set', full=True)
	interactiveelements = fields.ToManyField('api.InteractiveElementResource', 'interactiveelement_set', full=True)
	# staticelements = fields.ToManyField('api.StaticElementResource', 'staticelement_set')
	class Meta:
		queryset= Slide.objects.all()
		filtering = {
		"slug": ('exact'),
		}

class StaticElementResource(ModelResource):
	slide = fields.ForeignKey(SlideResource, 'slide')
	class Meta:
		queryset= StaticElement.objects.all()

class InteractiveElementResource(ModelResource):
	slide= fields.ForeignKey(SlideResource, 'slide')
	class Meta:
		queryset= InteractiveElement.objects.all()


		
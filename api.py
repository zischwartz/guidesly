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
	# staticelements = fields.ToManyField('api.StaticElementResource', 'staticelement_set')

	class Meta:
		queryset= Slide.objects.all()

		filtering = {
		"slug": ('exact'),
		}
		# http://127.0.0.1:8000/api/v1/slide/?format=json&slug=1
		# http://127.0.0.1:8000/api/v1/slide/?slug=1&format=json



class StaticElementResource(ModelResource):
	slide = fields.ForeignKey(SlideResource, 'slide')

	class Meta:
		queryset= StaticElement.objects.all().select_subclasses()


		
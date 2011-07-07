from tastypie.resources import ModelResource

from guides.models import *
from fileupload.models import UserFile
from tastypie import fields
from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS

class myUserAuthorization(Authorization):
	def is_authorized(self, request, object=None):
		return True
		# well that needs to be fixed TODO
	# def apply_limits(self, request, object_list):
	# 	if request and hasattr(request, 'user'):
	# 		return object_list.filter(owner__username=request.user.username)
	# 	return object_list.none()



class UserResource(ModelResource):
	class Meta:
		queryset= User.objects.all()
		# excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
		fields = ['id', 'username']
		allowed_methods = ['get']

		
class CardResource(ModelResource):
	staticelements = fields.ToManyField('api.StaticElementResource', 'staticelement_set', full=True)
	interactiveelements = fields.ToManyField('api.InteractiveElementResource', 'interactiveelement_set', full=True)
	class Meta:
		authorization = Authorization()
		# always_return_data = True
		# allowed_methods =   ['get', 'post', 'put', 'delete']
		# include_resource_uri =False
		queryset= Card.objects.all()
		filtering = {
		"slug": ('exact'),
		}


class UserFileResource(ModelResource):
	owner = fields.ForeignKey(UserResource, 'owner', full=True)
	class Meta:
		queryset= UserFile.objects.all()
		authorization= myUserAuthorization()
		excludes = ['created']
		# include_resource_uri =False
		filtering= {"type": ('exact'), "owner": ('exact')}

		
class StaticElementResource(ModelResource):
	card = fields.ForeignKey(CardResource, 'card')
	file = fields.ForeignKey(UserFileResource, 'file', full=True)
	class Meta:
		authorization = Authorization()
		queryset= StaticElement.objects.all()
		excludes = ['created']

class InteractiveElementResource(ModelResource):
	card= fields.ForeignKey(CardResource, 'card')
	class Meta:
		queryset= InteractiveElement.objects.all()
		
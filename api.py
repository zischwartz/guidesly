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
	def apply_limits(self, request, object_list):
		if request and hasattr(request, 'user'):
			return object_list.filter(owner__username=request.user.username)
		return object_list.none()



class UserResource(ModelResource):
	class Meta:
		queryset= User.objects.all()
		# excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
		fields = ['id', 'username']
		allowed_methods = ['get']
		authorization = Authorization()

		
class CardResource(ModelResource):
	staticelements = fields.ToManyField('api.StaticElementResource', 'staticelement_set', full=True, readonly=True, null=True )#, readonly=True))
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
	def hydrate_staticelements(self, bundle):
		from guides.log import *
		# logger=getlogger()		
		# 	logger.debug('XXXXYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYXXX')
		# 	logger.debug('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
		# 	logger.debug(bundle.data['staticelements'])
		
		statics = []
		# for el in bundle.data['staticelements']:
			# statics.append("id")
			# statics.append(el['resource_uri'])
		bundle.data['staticelements']=statics
		# logger.debug('*******************************************************')
		# logger.debug(bundle.data['staticelements'])
		return bundle
	
	# def hydrate_title(self, bundle):
	# 	import logging
	# 	logging.info("heyyyyyyyyyyyyyyyyyyyyy")
	# 	return bundle.obj.title.upper()
	
	# def hydrate_title(self, bundle):
	# 	list_of_statics= []
	# 	logging.info("heyy")
	# 	logging.info(bundle.data['title'])
	# 	return bundle.data['title'].lower()
		# for se in bundle.data['staticelements']:
			# list_of_se+=se[0]
		# bundle.data['staticelements'] = ["/api/v1/staticelement/1/", "/api/v1/staticelement/2"]
		# return bundle


class UserFileResource(ModelResource):
	# owner = fields.ForeignKey(UserResource, 'owner', full=True) //WORKS
	owner = fields.ForeignKey(UserResource, 'owner' )#, full=True)
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
		
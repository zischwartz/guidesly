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
	mediaelements = fields.ToManyField('api.MediaElementResource', 'mediaelement_set', full=True, readonly=True, null=True )#, readonly=True))
	inputelements = fields.ToManyField('api.InputElementResource', 'inputelement_set', full=True, readonly=True, null=True)
	class Meta:
		authorization = Authorization()
		# always_return_data = True
		# allowed_methods =   ['get', 'post', 'put', 'delete']
		# include_resource_uri =False
		queryset= Card.objects.all()
		filtering = {
		"slug": ('exact'),
		}
	def hydrate_mediaelements(self, bundle):
		# from guides.log import *
		# logger=getlogger()		
		# 	logger.debug('XXXXYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYXXX')
		# 	logger.debug('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
		# 	logger.debug(bundle.data['mediaelements'])
		
		emptylist = []
		# the below was totally unncessary, but a nice idea.
		# for el in bundle.data['mediaelements']:
			# statics.append("id")
			# statics.append(el['resource_uri'])
		bundle.data['mediaelements']=emptylist
		bundle.data['inputelements']=emptylist


		return bundle
	


class UserFileResource(ModelResource):
	owner = fields.ForeignKey(UserResource, 'owner' )#, full=True)
	class Meta:
		queryset= UserFile.objects.all()
		authorization= myUserAuthorization()
		excludes = ['created']
		# include_resource_uri =False
		filtering= {"type": ('exact'), "owner": ('exact')}

		
class MediaElementResource(ModelResource):
	card = fields.ForeignKey(CardResource, 'card')
	file = fields.ForeignKey(UserFileResource, 'file', full=True)
	class Meta:
		authorization = Authorization()
		queryset= MediaElement.objects.all()
		excludes = ['created']
		
class ActionResource(ModelResource):
	goto= fields.ForeignKey(CardResource, 'goto')
	class Meta:
		queryset= Action.objects.all()
		authorization = Authorization()
		include_resource_uri =False #having this false was screwing things up


class InputElementResource(ModelResource):
	card= fields.ForeignKey(CardResource, 'card')
	default_action= fields.ToOneField(ActionResource, 'default_action', null=True, full=True) #, full=True) #full being true made a mess on PUT 
	class Meta:
		queryset= InputElement.objects.all()
		authorization = Authorization()


		# always_return_data = True #so we can get the Action's resource uri

	# def save_related(self, bundle):
	# 	from guides.log import *
	# 	logger=getlogger()
	# 	logger.debug("HELLO!")
	# 	logger.debug(self)
	# 	logger.debug(bundle)
		
	# def hydrate(self, bundle):
		# bundle.data['']
		
		# from guides.log import *
		# logger=getlogger()		
		# logger.debug('XXXXYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYXXX')
		# logger.debug(bundle)
		# a = ActionResource()
		# action_uri= a.get_resource_uri(bundle.obj.default_action) #get the uri of the default_action of the input
		# bundle.data['default_action']=action_uri
		# return bundle

# Maybe just start using default goto for now.
#  Profile.objects.get_or_create(user=instance)

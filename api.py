from tastypie.resources import ModelResource

from guides.models import *
from thef.models import *
from fileupload.models import UserFile, Image
# from photologue.models import Photo

from tastypie import fields
from django.contrib.auth.models import User

from tastypie.authentication import BasicAuthentication
# from tastypie.authentication import DigestAuthentication

from tastypie.authorization import Authorization
from tastypie.authorization import DjangoAuthorization

from tastypie.constants import ALL, ALL_WITH_RELATIONS
from django.core.urlresolvers import reverse
from guides.log import *
logger=getlogger()


class myUserAuthorization(Authorization):
	def is_authorized(self, request, object=None):
		return True
# 		# well that needs to be fixed TODO
# 	def apply_limits(self, request, object_list):
# 		if request and hasattr(request, 'user'):
# 			return object_list.filter(owner__username=request.user.username)
# 		return object_list.none()



class UserResource(ModelResource):
	class Meta:
		queryset= User.objects.all()
		# excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
		fields = ['id', 'username']
		allowed_methods = ['get']
		# authentication = BasicAuthentication()
		# authorization = DjangoAuthorization()
		authorization = Authorization()
		

		
class CardResource(ModelResource):
	mediaelements = fields.ToManyField('api.MediaElementResource', 'mediaelement_set', full=True, readonly=True, null=True )#, readonly=True))
	inputelements = fields.ToManyField('api.InputElementResource', 'inputelement_set', full=True, readonly=True, null=True)
	mappointelements = fields.ToManyField('api.MapPointElementResource', 'mappointelement_set', full=True, readonly=True, null=True)
	guide = fields.ForeignKey('api.GuideResource', 'guide', null=True)
	primary_media = fields.ForeignKey('api.MediaElementResource', 'primary_media', null=True, blank=True) #, full= True)
	class Meta:
		# authentication = BasicAuthentication()
		# authorization = DjangoAuthorization()
		
		# authentication = BasicAuthentication()
		authorization = Authorization()
		
		queryset= Card.objects.all()
		filtering = {
		"slug": ('exact'),
		}
		
	
	# def hydrate_mediaelements(self, bundle):	
	# 	emptylist = []
	# 	# the below was totally unncessary, but a nice idea.
	# 	# for el in bundle.data['mediaelements']:
	# 		# statics.append("id")
	# 		# statics.append(el['resource_uri'])
	# 	bundle.data['mediaelements']=emptylist
	# 	bundle.data['inputelements']=emptylist
	# 	return bundle
	
class SmallCardResource(ModelResource):
	guide = fields.ForeignKey('api.GuideResource', 'guide')
	primary_media = fields.ForeignKey('api.MediaElementResource', 'primary_media', null=True, blank=True, full=True, readonly=True)
	class Meta:
		excludes = ['created', 'modified']
		# include_absolute_url =True
		authorization = Authorization()
		queryset= Card.objects.all()
		filtering= {"guide": ALL_WITH_RELATIONS,}
	
	# def hydrate(self, bundle):
		# logger.info("HYDRATEEEEd")
		# logger.info(bundle.data)
		# bundle.data['edit_url'] = None
		# bundle.data['absolute_url'] = None
	def dehydrate(self, bundle):
		# logger.info("dehydrated-------------")
		# logger.info(bundle.data)
		bundle.data['edit_url'] = reverse('EditCard', kwargs={'gslug':bundle.obj.guide.slug, 'id': bundle.obj.id})
		bundle.data['absolute_url'] = bundle.obj.get_absolute_url()
		bundle.data['thumb'] = bundle.obj.get_thumb()
		return bundle

class GuideResource(ModelResource):
	cards = fields.ToManyField('api.SmallCardResource', 'card_set', full=True, null=True, readonly=True) #eventually get rid of readonly true
	class Meta:
		authorization = Authorization()
		excludes = ['created', 'modified']
		queryset= Guide.objects.all()
		filtering= {"slug": ('exact'), "owner": ('exact')}

class FullGuideResource(ModelResource):
	cards = fields.ToManyField('api.CardResource', 'card_set', full=True, null=True, readonly=True) #eventually get rid of readonly true
	class Meta:
		authorization = Authorization()
		excludes = ['created', 'modified']
		queryset= Guide.objects.all()
		filtering= {"slug": ('exact'), "owner": ('exact')}


class SmallGuideResource(ModelResource):
	class Meta:
		authorization = Authorization()
		excludes = ['created', 'modified']
		queryset= Guide.objects.all()
		filtering= {"slug": ('exact'), "owner": ('exact')}
		
	def dehydrate(self, bundle):
		# logger.info("dehydrated-------------")
		# g = GuideResource()
		bundle.data['resource_uri'] = bundle.obj.resource_uri
		# bundle.data['resource_uriz'] = g.get_resource_uri(bundle.obj) # this should work...
		return bundle

class ImageResource(ModelResource):
	class Meta:
		authorization = Authorization()
		queryset= Image.objects.all()


class UserFileResource(ModelResource):
	owner = fields.ForeignKey(UserResource, 'owner',  null=True)#, full=True)
	image = fields.ForeignKey(ImageResource, 'image', null=True)#, full=True)

	class Meta:
		queryset= UserFile.objects.all()
		# authorization= myUserAuthorization()
		excludes = ['created']
		# include_resource_uri =False
		filtering= {"type": ('exact'), "owner": ('exact')}

		
class MediaElementResource(ModelResource):
	card = fields.ForeignKey(CardResource, 'card')
	file = fields.ForeignKey(UserFileResource, 'file', full=True, null=True, readonly=True)#  #added readonly this, it won't change, and was slowing down PUT massively
	class Meta:
		authorization = Authorization()
		queryset= MediaElement.objects.all()
		excludes = ['created']
		
class ActionResource(ModelResource):
	goto= fields.ForeignKey(SmallCardResource, 'goto', null=True) #made it smallCard instead of card
	class Meta:
		queryset= Action.objects.all()
		# authorization = Authorization()
		include_resource_uri =False #having this false was screwing things up
		
	def dehydrate(self, bundle):
		bundle.data['dest_slug'] = bundle.obj.get_dest_slug()
		return bundle


class InputElementResource(ModelResource):
	card= fields.ForeignKey(CardResource, 'card')
	default_action= fields.ToOneField(ActionResource, 'default_action', null=True, full=True) #, full=True) #full being true made a mess on PUT 
	class Meta:
		queryset= InputElement.objects.all()
		# authorization = Authorization()
		filtering= {"type": ('exact'), "card": ('exact')}
		
		
class MapPointElementResource(ModelResource):
	default_action= fields.ToOneField(ActionResource, 'default_action', null=True, full=True)  
	card= fields.ForeignKey(CardResource, 'card')
	class Meta:
		queryset= MapPointElement.objects.all()
		# authorization = Authorization()




class TheFResource(ModelResource):
	class Meta:
		queryset = theF.objects.all()
		# authorization = Authorization()

		
	# def full_hydrate(self, bundle):
	# 	# bundle.data['']
	# 	
	# 	from guides.log import *
	# 	logger=getlogger()		
	# 	logger.debug('XXXXYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYXXX')
	# 	logger.debug(bundle)
	# 	# a = ActionResource()
	# 	# action_uri= a.get_resource_uri(bundle.obj.default_action) #get the uri of the default_action of the input
	# 	# bundle.data['default_action']=action_uri
	# 	return bundle

# Maybe just start using default goto for now.
#  Profile.objects.get_or_create(user=instance)

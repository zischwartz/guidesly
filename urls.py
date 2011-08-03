from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings			  
from django.views.generic.simple import direct_to_template 

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from api import *

from guides.views import *


v1_api = Api(api_name='v1')

v1_api.register(MediaElementResource())
v1_api.register(ActionResource())
v1_api.register(InputElementResource())
v1_api.register(CardResource())
v1_api.register(UserFileResource())
v1_api.register(UserResource())
v1_api.register(SmallCardResource())
v1_api.register(GuideResource())



urlpatterns = patterns('',
	# Examples:
	# (r'^$', ListView.as_view(model=Guide)),
	(r'^$', GuideListView),
	url(r'^g/(?P<slug>[^/]+)/?$', GuideDetailView, name='GuideDetailView'),
	url(r'^g/(?P<gslug>[^/]+)/(?P<slug>[^/]+)/?$', CardDetailView, name='CardDetailView'),
	url(r'^n/(?P<gslug>[^/]+)/(?P<cnumber>[^/]+)/?$', CardDetailView, name='CardDetailViewByNum'),
	url(r'^c/(?P<id>[^/]+)/?$', CardDetailViewById, name='CardDetailViewById'),	  

	#url(r'^profiles/', include('profiles.urls')),		
	#url(r'^profiles/edit', 'profiles.views.edit_profile'),
	
	url(r'create/?$', CreateGuide, name='CreateGuide'),
	url(r'create/(?P<gslug>[^/]+)/?$', EditGuide, name='EditGuide'),
	url(r'create/(?P<gslug>[^/]+)/add/?$', BuildCard, name='BuildCard'),
	url(r'create/(?P<gslug>[^/]+)/(?P<id>[^/]+)/?$', EditCard, name='EditCard'),
	# url(r'create/(?P<gslug>[^/]+)/(?P<slug>[^/]+)/addmedia$', AddMediaElement, name='AddMediaElement'),
	# url(r'create/(?P<gslug>[^/]+)/(?P<slug>[^/]+)/editmedia/(?P<elementid>[^/]+)$', EditMediaElement, name='EditMediaElement'),
	# url(r'create/(?P<gslug>[^/]+)/(?P<slug>[^/]+)/addinput$', AddInputElement, name='AddInputElement'),
	# url(r'create/(?P<gslug>[^/]+)/(?P<slug>[^/]+)/editinput/(?P<elementid>[^/]+)$', EditInputElement, name='EditInputElement'),
	url(r'^upload/', include('fileupload.urls')),
	(r'^api/', include(v1_api.urls)),

	# (r'^guide/(?P<slug>[^/]+)/?$', GuideDetailView),
	# url(r'^learny/', include('learny.foo.urls')),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),		  
	url(r'^accounts/', include('invitation.urls')),
	url(r'^accounts/', include('registration.backends.default.urls')), 
	url(r'^accounts/', include('registration.urls')),				
	url(r'^accounts/', include('registration.auth_urls')),    
    #url(r'^accounts/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'},),      
	url(r'^accounts/', include('accounts.urls')),	    
	url(r'^user/', include('accounts.urls')),  
  

)


urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
	urlpatterns += patterns('',
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
			'document_root': settings.MEDIA_ROOT,
		}),
   )
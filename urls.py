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
v1_api.register(UserResource())

v1_api.register(MediaElementResource())
v1_api.register(ActionResource())
v1_api.register(InputElementResource())
v1_api.register(MapPointElementResource())
v1_api.register(MapElementResource())
v1_api.register(CardResource())
v1_api.register(ImageResource())
v1_api.register(UserFileResource())
v1_api.register(SmallCardResource())
v1_api.register(GuideResource())
v1_api.register(TheFResource())




urlpatterns = patterns('',
    # Examples:
    # (r'^$', ListView.as_view(model=Guide)),

    (r'^$', Landing),
    (r'^home/$', GuideListView),
    url(r'^g/(?P<slug>[^/]+)/?$', GuideDetailView, name='GuideDetailView'),
    url(r'^s/(?P<gslug>[^/]+)/(?P<slug>[^/]+)/?$', CardInStack),
    url(r'^g/(?P<gslug>[^/]+)/(?P<slug>[^/]+)/?$', CardDetailView, name='CardDetailView'),
    url(r'^n/(?P<gslug>[^/]+)/(?P<cnumber>[^/]+)/?$', CardDetailView, name='CardDetailViewByNum'),
    url(r'^c/(?P<gslug>[^/]+)/(?P<id>[^/]+)/?$', CardDetailView, name='CardDetailViewById'),
    url(r'^i/(?P<id>[^/]+)/?$', CardDetailViewByIdRedirect, name='CardDetailViewByIdRedirect'),

	url(r'create/?$', CreateGuide, name='CreateGuide'),
	url(r'create/(?P<gslug>[^/]+)/?$', EditGuide, name='EditGuide'),
	url(r'create/(?P<gslug>[^/]+)/add/?$', BuildCard, name='BuildCard'),
	url(r'create/(?P<gslug>[^/]+)/addfloating/?$', BuildFloatingCard, name='BuildFloatingCard'),
	url(r'create/(?P<gslug>[^/]+)/(?P<id>[^/]+)/?$', EditCard, name='EditCard'),
	url(r'^upload/', include('fileupload.urls')),
	(r'^api/', include(v1_api.urls)),

	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),		  
	url(r'^accounts/', include('invitation.urls')),
	url(r'^accounts/', include('registration.backends.default.urls')), 
	url(r'^accounts/', include('registration.urls')),				
	url(r'^accounts/', include('registration.auth_urls')),        
	url(r'^accounts/', include('accounts.urls')),	    
	url(r'^user/', include('accounts.urls')),  
  
	# url(r'^photologue/', include('photologue.urls')),

)


urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
	urlpatterns += patterns('',
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
			'document_root': settings.MEDIA_ROOT,
		}),
   )
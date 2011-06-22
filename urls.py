from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from guides.views import *


urlpatterns = patterns('',
    # Examples:
    # (r'^$', ListView.as_view(model=Guide)),
    (r'^$', GuideListView),
    url(r'^g/(?P<slug>[^/]+)/?$', GuideDetailView, name='GuideDetailView'),
    url(r'^g/(?P<gslug>[^/]+)/(?P<slug>[^/]+)/?$', SlideDetailView, name='SlideDetailView'),
    
    url(r'create/?$', CreateGuide, name='CreateGuide'),
    url(r'create/(?P<gslug>[^/]+)/?$', EditGuide, name='EditGuide'),
    url(r'create/(?P<gslug>[^/]+)/add/?$', BuildSlide, name='BuildSlide'),
    url(r'create/(?P<gslug>[^/]+)/(?P<slug>[^/]+)/?$', EditSlide, name='EditSlide'),
    url(r'create/(?P<gslug>[^/]+)/(?P<slug>[^/]+)/addstatic$', AddStaticElement, name='AddStaticElement'),
    url(r'create/(?P<gslug>[^/]+)/(?P<slug>[^/]+)/editstatic/(?P<elementid>[^/]+)$', EditStaticElement, name='EditStaticElement'),
    url(r'create/(?P<gslug>[^/]+)/(?P<slug>[^/]+)/addinteractive$', AddInteractiveElement, name='AddInteractiveElement'),


    # (r'^guide/(?P<slug>[^/]+)/?$', GuideDetailView),
    # url(r'^learny/', include('learny.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
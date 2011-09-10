from django.conf import settings
from django.conf.urls.defaults import *
from videologue.models import Gallery, Video
from django.db.models import Count

gallery_qs = Gallery.objects.filter(is_public=True)

# Number of random images from the gallery to display.
SAMPLE_SIZE = ":%s" % getattr(settings, 'GALLERY_SAMPLE_SIZE', 5)

# galleries
gallery_args = {
    'date_field': 'date_added', 'allow_empty': True, 'queryset': gallery_qs,
    'extra_context': { 'sample_size':SAMPLE_SIZE, 'FLOWPLAYER': settings.FLOWPLAYER }
}
urlpatterns = patterns('django.views.generic.date_based',

    url(r'^gallery/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$', 'object_detail', {
        'date_field': 'date_added', 'slug_field': 'title_slug', 'queryset': gallery_qs,
        'extra_context':{
            'sample_size':SAMPLE_SIZE,
            'FLOWPLAYER': settings.FLOWPLAYER
            }
        },
    name='vl-gallery-detail'),

    url(r'^gallery/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', gallery_args, name='vl-gallery-archive-day'),
    url(r'^gallery/(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', gallery_args, name='vl-gallery-archive-month'),
    url(r'^gallery/(?P<year>\d{4})/$', 'archive_year', gallery_args, name='vl-gallery-archive-year'),
    url(r'^gallery/?$', 'archive_index', gallery_args, name='vl-gallery-archive'),
)

urlpatterns += patterns('django.views.generic.list_detail',

    url(r'^gallery/(?P<slug>[\-\d\w]+)/$', 'object_detail', { 'slug_field': 'title_slug', 'queryset': gallery_qs,
        'extra_context':{
            'sample_size':SAMPLE_SIZE,
            'FLOWPLAYER': settings.FLOWPLAYER
            }
        }, name='vl-gallery'),

    url(r'^gallery/page/(?P<page>[0-9]+)/$', 'object_list', { 'queryset': gallery_qs, 'allow_empty': True, 'paginate_by': 5,
        'extra_context': {
            'sample_size': SAMPLE_SIZE,
            'FLOWPLAYER': settings.FLOWPLAYER
            }
        }, name='vl-gallery-list'),
)

video_qs = Video.objects.filter(flv_video__isnull=False, is_public=True)

video_args = {'date_field': 'date_added', 'allow_empty': True, 'queryset': video_qs,
    'extra_context': { 'FLOWPLAYER': settings.FLOWPLAYER }
}
urlpatterns += patterns('django.views.generic.date_based',

    url(r'^video/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$', 'object_detail', {'date_field': 'date_added', 'slug_field': 'title_slug', 'queryset': video_qs}, name='vl-video-detail'),
    url(r'^video/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', video_args, name='vl-video-archive-day'),
    url(r'^video/(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', video_args, name='vl-video-archive-month'),
    url(r'^video/(?P<year>\d{4})/$', 'archive_year', video_args, name='vl-video-archive-year'),
    url(r'^video/$', 'archive_index', video_args, name='vl-video-archive'),
)

urlpatterns += patterns('django.views.generic.list_detail',

    url(r'^video/(?P<slug>[\-\d\w]+)/$', 'object_detail', {'slug_field': 'title_slug', 'queryset': video_qs,
            'extra_context': {
                'FLOWPLAYER': settings.FLOWPLAYER
            }
        },
    name='vl-video'),

    url(r'^video/page/(?P<page>[0-9]+)/$', 'object_list', {'queryset': video_qs, 'allow_empty': True, 'paginate_by': 20,
            'extra_context': {
                'FLOWPLAYER': settings.FLOWPLAYER
            }
        },
    name='vl-video-list'),
)



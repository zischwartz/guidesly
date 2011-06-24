from django.conf.urls.defaults import *
from views import UserFileCreateView, UserFileDeleteView

urlpatterns = patterns('',
    (r'^new/$', UserFileCreateView.as_view(), {}, 'upload-new'),
    (r'^delete/(?P<slug>.+)$', UserFileDeleteView.as_view(), {}, 'upload-delete'),
)


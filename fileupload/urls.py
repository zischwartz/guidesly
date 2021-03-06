from django.conf.urls.defaults import *
from views import UserFileCreateView, UserFileDeleteView, UserFileListView

urlpatterns = patterns('',
    (r'^new/$', UserFileCreateView.as_view(), {}, 'upload-new'),
    (r'^delete/(?P<slug>.+)$', UserFileDeleteView.as_view(), {}, 'upload-delete'),
    (r'^list/(?P<file_type>.+)$', UserFileListView.as_view(), {}, 'upload-list'),
)


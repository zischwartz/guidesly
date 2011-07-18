from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    (r'^profile/$', YourProfile),
    # (r'^profile/$', UserFileCreateView.as_view(), {}, 'upload-new'),

)

urlpatterns += patterns('django.contrib.auth',
    (r'^login/$','views.login', {'template_name': 'admin/login.html'}),
    (r'^logout/$','views.logout'),
)
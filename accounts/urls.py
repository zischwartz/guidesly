from django.conf.urls.defaults import *
from views import *        
from accounts import views   
from django.contrib.auth import views as auth_views    
  

#urlpatterns = patterns('',
#    (r'^profile/$', YourProfile),
    #(r'^profile/$', UserFileCreateView.as_view(), {}, 'upload-new'),

#)        


urlpatterns = patterns('',	
	url(r'^new/$',
		views.create_profile,
		name='profiles_create_profile'),
	url(r'^edit/$',
		views.edit_profile,
		name='profiles_edit_profile'),
	url(r'^(?P<username>\w+)/$',
		views.profile_detail,
		name='profiles_profile_detail'),
	url(r'^$',
		views.profile_list,
		name='profiles_profile_list'), 
	url(r'^welcome/$', 
		views.welcome,
		name='profiles_welcome'),
	                                   
)
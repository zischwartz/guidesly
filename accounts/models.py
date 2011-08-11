from django.db import models

from django.conf import settings
from django.contrib.auth.models import User	 


from guides.models import Guide 
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

class UserProfile(models.Model):

	user = models.ForeignKey(User, unique=True, verbose_name=_('user')) 
	is_new_here = models.BooleanField(default=True)
	name = models.CharField(_('name'), max_length=50, null=True, blank=True)
	about = models.TextField(_('about'), null=True, blank=True)
	location = models.CharField(_('location'), max_length=50, null=True, blank=True)
	website = models.URLField(_('website'), null=True, blank=True, verify_exists=False)	  
	viewings = models.ManyToManyField(Guide, through='Viewing', related_name="viewingByUser")
	upvote = models.ManyToManyField(Guide, through='Upvote', related_name="upvoteByUser")
	
	def __unicode__(self):
		return self.user.username
	
	def get_absolute_url(self):
		return ('profile_detail', None, {'username': self.user.username})
	get_absolute_url = models.permalink(get_absolute_url)
	
	class Meta:
		verbose_name = _('profile')
		verbose_name_plural = _('profiles')	  
                                                  

	

class Viewing(models.Model):
	userprofile = models.ForeignKey(UserProfile, related_name="userWhoViewed")
	guide = models.ForeignKey(Guide)
	date = models.DateTimeField(auto_now=True)
	card_num = models.IntegerField(blank=True,null=True)
	hidden = models.BooleanField(default=False)

class Upvote(models.Model):
	userprofile = models.ForeignKey(UserProfile, related_name="userWhoVoted")
	guide = models.ForeignKey(Guide)
	card_num = models.IntegerField(blank=True,null=True)
	date=models.DateTimeField(auto_now=True)	 

	

def create_profile(sender, instance=None, **kwargs):
	if instance is None:
		return
	profile, created = UserProfile.objects.get_or_create(user=instance)
                                          

post_save.connect(create_profile, sender=User)  

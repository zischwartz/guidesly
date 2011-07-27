from django.db import models
from django.contrib.auth.models import User

from guides.models import Guide
# Create your models here.


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	viewings = models.ManyToManyField(Guide, through='Viewing', related_name="viewingByUser")
	upvote = models.ManyToManyField(Guide, through='Upvote', related_name="upvoteByUser")
	
class Viewing(models.Model):
	userprofile = models.ForeignKey(UserProfile, related_name="userWhoViewed")
	guide = models.ForeignKey(Guide)
	models.DateTimeField(auto_now=True)
	card_num = models.IntegerField(blank=True, null=True)
	hidden = models.BooleanField(default=False)

class Upvote(models.Model):
	userprofile = models.ForeignKey(UserProfile, related_name="userWhoVoted")
	guide = models.ForeignKey(Guide)
	models.DateTimeField(auto_now=True)
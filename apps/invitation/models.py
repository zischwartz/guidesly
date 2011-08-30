#import os
import random
import datetime
import re 
import sha

from django.conf import settings
from django.utils.http import int_to_base36
from django.utils.hashcompat import sha_constructor
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models  
from django.db import transaction
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site, RequestSite

from registration.models import SHA1_RE


class InvitationKeyManager(models.Manager):
	def get_key(self, invitation_key):
		
		## Return InvitationKey
		
	   
		if not SHA1_RE.search(invitation_key):
			return None
		
		try:
			key = self.get(key=invitation_key)
		except self.model.DoesNotExist:
			return None
		
		return key
		
	def is_key_valid(self, invitation_key):
		invitation_key = self.get_key(invitation_key)
		return invitation_key and invitation_key.is_usable()  
	  

	def create_invitation(self, user):
	   
		
	   ## The key for the ``InvitationKey`` will be a SHA1 hash, generated 
		##from a combination of the ``User``'s username and a random salt.
   
		salt = sha_constructor(str(random.random())).hexdigest()[:5]
		key = sha_constructor("%s%s%s" % (datetime.datetime.now(), salt, user.username)).hexdigest()
		return self.create(from_user=user, key=key)

	def remaining_invitations_for_user(self, user):
		invitation_user, created = InvitationUser.objects.get_or_create(
			inviter=user,
			defaults={'invitations_remaining': settings.INVITATIONS_PER_USER})
		return invitation_user.invitations_remaining

	def delete_expired_keys(self):
		for key in self.all():
			if key.key_expired():
				key.delete()


class InvitationKey(models.Model):		   
	
	ACTIVATED = u"ALREADY_USED"	 
	
	date_invited = models.DateTimeField(_('date invited'), 
									   default=datetime.datetime.now)
	from_user = models.ForeignKey(User, 
								  related_name='invitations_sent')
	registrant = models.ForeignKey(User, null=True, blank=True, 
								  related_name='invitations_used') 

	key = models.CharField(_('invitation key'), max_length=40)	
	
	
	objects = InvitationKeyManager()
	
	def __unicode__(self):
		return u"Invitation from %s on %s" % (self.from_user.username, self.date_invited)
	
  
	
	def key_expired(self):	   
		expiration_date = datetime.timedelta(days=settings.ACCOUNT_INVITATION_DAYS) 
		return self.key == self.ACTIVATED or (self.date_invited + expiration_date <= datetime.datetime.now())
	key_expired.boolean = True		

	def is_usable(self):

		return self.registrant is None and not self.key_expired()
	
	def mark_used(self, registrant):
		self.registrant = registrant   
		self.save()
  
	def send_to(self, email):
		current_site = Site.objects.get_current()
		
		subject = render_to_string('invitation/invitation_email_subject.txt',
								   { 'site': current_site, 
									 'invitation_key': self })
	  
		subject = ''.join(subject.splitlines())
		
		message = render_to_string('invitation/invitation_email.txt',
								   { 'invitation_key': self,
									 'expiration_days': settings.ACCOUNT_INVITATION_DAYS,
									 'site': current_site })
		
		send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

		
class InvitationUser(models.Model):
	inviter = models.ForeignKey(User, unique=True)
	invitations_remaining = models.IntegerField()

	def __unicode__(self):
		return u"InvitationUser for %s" % self.inviter.username

	
def user_post_save(sender, instance, created, **kwargs):
	if created:
		invitation_user = InvitationUser()
		invitation_user.inviter = instance
		invitation_user.invitations_remaining = settings.INVITATIONS_PER_USER
		invitation_user.save()

models.signals.post_save.connect(user_post_save, sender=User)

def invitation_key_post_save(sender, instance, created, **kwargs):
	if created:
		invitation_user = InvitationUser.objects.get(inviter=instance.from_user)
		remaining = invitation_user.invitations_remaining
		invitation_user.invitations_remaining = remaining-1
		invitation_user.save()

models.signals.post_save.connect(invitation_key_post_save, sender=InvitationKey)		  



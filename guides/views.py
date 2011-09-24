# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from models import *
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime

from django.views.generic import ListView, DetailView
from forms import *
from django.core.urlresolvers import reverse

from django.contrib import messages

from log import getlogger
logger=getlogger()
# logger.debug("---------------")

from django.utils import simplejson
from fileupload.models import UserFile
from api import CardResource, SmallCardResource, GuideResource, MediaElementResource


from decorators import require_owner, require_published_and_public
from django.contrib.auth.decorators import login_required

# Viewing Guides
# -------------------------

def Landing (request): 
	if request.user.is_authenticated():		  
		return HttpResponseRedirect('/home/')
	return render_to_response("site/landing.html", locals(), context_instance=RequestContext(request))
	

@login_required
def Home (request):
	if request.user.is_authenticated():
		your_guides= request.user.guide_set.all()
	guide_list = Guide.objects.filter(published=True, private=False) #add accepted_to_cat	
	return render_to_response("site/home.html", locals(), context_instance=RequestContext(request))


def GuideDetailView (request, slug):
	guide = get_object_or_404(Guide, slug=slug)
	if guide.first_card:
		return HttpResponseRedirect(reverse('CardDetailViewByIdRedirect', kwargs={'id': guide.first_card.id}))
	card_list= guide.card_set.all()
	return render_to_response("enjoy/guide_detail.html", locals(), context_instance=RequestContext(request))

@require_published_and_public
def CardInStack (request, gslug, slug):
	requested_card = get_object_or_404(Card, guide__slug=gslug, slug=slug)
	guide = get_object_or_404(Guide, slug=gslug)
	return render_to_response("enjoy/card_in_stack.html", locals(), context_instance=RequestContext(request))
	

def SecretGuideView (request, private_url):
	import re
	SHA1_RE = re.compile('^[a-f0-9]{40}$')
	if not SHA1_RE.search(private_url):
		return HttpResponseRedirect('/')
	guide = get_object_or_404(Guide, private_url = private_url)
	if guide.first_card:
		return HttpResponseRedirect(reverse('SecretCardView', kwargs={'private_url': private_url, 'slug': guide.first_card.slug}))
	
	return render_to_response("enjoy/card_in_stack.html", locals(), context_instance=RequestContext(request))

def SecretCardView (request, private_url, slug):
	import re
	SHA1_RE = re.compile('^[a-f0-9]{40}$')
	if not SHA1_RE.search(private_url):
		return HttpResponseRedirect('/')
	guide = get_object_or_404(Guide, private_url = private_url)
	requested_card = get_object_or_404(Card, guide=guide, slug=slug)
	return render_to_response("enjoy/card_in_stack.html", locals(), context_instance=RequestContext(request))



def CardDetailViewByIdRedirect (request, id):
	card = get_object_or_404(Card, id=id)
	return HttpResponseRedirect(card.get_absolute_url())


# Creating Guides
# -------------------------

@login_required
def CreateGuide (request):
	if request.method == 'POST':
		logger.info('posted')
		form = GuideForm(request.POST)
		if form.is_valid():
			g =form.save()
			return HttpResponseRedirect(reverse('BuildCard', kwargs={'gslug':g.slug}))
		else:
			messages.add_message(request, messages.INFO, form.errors)
			return render_to_response("create/create_guide.html", locals(), context_instance=RequestContext(request) )
	else:
		form = GuideForm()
	return render_to_response("create/create_guide.html", locals(), context_instance=RequestContext(request) )

@require_owner
def BuildCard (request, gslug):
	your_guide=get_object_or_404(Guide, slug=gslug)
	if your_guide.is_linear:
		s = Card(guide=your_guide)
	else:
		s = Card(guide=your_guide, is_floating_card=True)
	s.firstsave()
	return HttpResponseRedirect(reverse('EditCard', kwargs={'gslug':gslug, 'id': s.id}))

@require_owner
def BuildFloatingCard (request, gslug):
	s = Card(guide=get_object_or_404(Guide, slug=gslug), is_floating_card=True)
	s.firstsave()
	return HttpResponseRedirect(reverse('EditCard', kwargs={'gslug':gslug, 'id': s.id}))


@require_owner
def EditCard (request, gslug, id):
	is_fluid =1
	card = get_object_or_404(Card, guide__slug=gslug, id=id)
	cr = CardResource()
	if not card.is_floating_card:
		prev_card = card.guide.get_prev_card(card)
		next_card = card.guide.get_next_card(card)	

	card_bundle= cr.build_bundle(obj=card, request=request)
	card_json= cr.serialize(request, cr.full_dehydrate(card_bundle), 'application/json') #with newer version, full dehyrate ur_bundle
	# logger.info(card_json)
	
	mr = MediaElementResource()
	if card.primary_media is not None:
		primary_media_bundle= mr.build_bundle(obj=card.primary_media, request=request)
		primary_media_json = mr.serialize(request, mr.full_dehydrate(primary_media_bundle),'application/json' )

	
	#should get the guide instead, that has the relevant card info and would be more consistant TODO delete above and impliment the below
	guide = get_object_or_404(Guide, slug=gslug)
	g = GuideResource()
	guide_bundle= g.build_bundle(obj=guide, request=request)
	guide_json = g.serialize(request, g.full_dehydrate(guide_bundle), 'application/json')
	
	return render_to_response("create/edit_card.html", locals(), context_instance=RequestContext(request))


@require_owner
def EditGuide (request, gslug):
	guide = get_object_or_404(Guide, slug=gslug)
	if request.method == 'POST':
		form = GuideForm(request.POST, instance=guide)
		if form.is_valid():
			g =form.save()
			return render_to_response("create/edit_guide.html", locals(), context_instance=RequestContext(request))
	else:
		form = GuideForm(instance= guide)
		g = GuideResource()
		guide_bundle= g.build_bundle(obj=guide, request=request)
		guide_json = g.serialize(request, g.full_dehydrate(guide_bundle), 'application/json')
		
	return render_to_response("create/edit_guide.html", locals(), context_instance=RequestContext(request))



@require_owner
def PublishGuide (request, gslug):
	guide = get_object_or_404(Guide, slug=gslug)
	if request.method == 'POST':
		form = PublishForm(request.POST, instance=guide)
		if form.is_valid():
			messages.add_message(request, messages.INFO, 'Guide Published!')
			g =form.save()
			if g.private:
				g.private_url= CreatePrivateURL(g.slug)
				g.save()
			return HttpResponseRedirect(reverse('EditGuide', kwargs={'gslug':gslug}))
			# return render_to_response("create/publish_guide.html", locals(), context_instance=RequestContext(request))
		else:
			messages.add_message(request, messages.INFO, form.errors)
			return render_to_response("create/publish_guide.html", locals(), context_instance=RequestContext(request))
			
	else:
		form = PublishForm(instance= guide)
	return render_to_response("create/publish_guide.html", locals(), context_instance=RequestContext(request))
	
	

	
	
#UTILITIES

def CreatePrivateURL(gslug):
	import hashlib
	from django.utils.hashcompat import sha_constructor
	import random
	import re
	m = hashlib.md5()
	m.hexdigest()
	salt = sha_constructor(str(random.random())).hexdigest()[:5]
	key = sha_constructor("%s%s%s" % (datetime.datetime.now(), salt, gslug)).hexdigest()
	return(key)

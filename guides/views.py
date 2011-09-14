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
from django.contrib.auth.decorators import login_required


# Viewing Guides
# -------------------------

def Landing (request): 
	if request.user.is_authenticated():		  
		guide_list = Guide.objects.all()
		your_guides= request.user.guide_set.all()
		return render_to_response("site/home.html", locals(), context_instance=RequestContext(request))   	
	return render_to_response("site/landing.html", locals(), context_instance=RequestContext(request))
	

@login_required
def GuideListView (request):
	if request.user.is_authenticated():
		your_guides= request.user.guide_set.all()
	guide_list = Guide.objects.all()
	return render_to_response("site/home.html", locals(), context_instance=RequestContext(request))


def GuideDetailView (request, slug):
	guide = get_object_or_404(Guide, slug=slug)
	if guide.first_card:
		return HttpResponseRedirect(reverse('CardDetailViewByIdRedirect', kwargs={'id': guide.first_card.id}))
		
	card_list= guide.card_set.all()
	return render_to_response("enjoy/guide_detail.html", locals(), context_instance=RequestContext(request))


# def CardInStack (request, gslug, slug):
def CardInStack (request, gslug):
	# current_card = get_object_or_404(Card, guide__slug=gslug, slug=slug)
	guide = get_object_or_404(Guide, slug=gslug)
	return render_to_response("enjoy/card_in_stack.html", locals(), context_instance=RequestContext(request))
	
	
	

def CardDetailView (request, gslug, id=None, slug=None, cnumber=None):
	if slug:
		card = get_object_or_404(Card, guide__slug=gslug, slug=slug)
	elif cnumber:
		card = get_object_or_404(Card, guide__slug=gslug, card_number=cnumber)		
	elif id:
		card = get_object_or_404(Card, id=id)
	
	images = []
	audio= None
	for element in card.mediaelement_set.all():
		if element.type=='image':
			images.append(element)
		if element.type == 'audio':
			audio=element
	# media_elements = card.mediaelement_set.all()
	input_elements=card.inputelement_set.all()
	map_elements=card.mapelement_set.all()
	primary_media=card.primary_media
	if not card.is_floating_card:
		prev_card = card.guide.get_prev_card(card)
		next_card = card.guide.get_next_card(card)
	return render_to_response("enjoy/card.html", locals(), context_instance=RequestContext(request))


def CardDetailViewByIdRedirect (request, id):
	card = get_object_or_404(Card, id=id)
	return HttpResponseRedirect(card.get_absolute_url())

	# if card.slug:
		# return HttpResponseRedirect(reverse('CardDetailView', kwargs={'gslug':card.guide.slug, 'slug': card.slug}))
	# elif card.card_number:
		# return HttpResponseRedirect(reverse('CardDetailViewByNum', kwargs={'gslug':card.guide.slug, 'cnumber': card.card_number}))
	# else:
		# return HttpResponseRedirect(reverse('CardDetailViewById', kwargs={'gslug':card.guide.slug, 'id': card.id}))



# Creating Guides
# -------------------------
@login_required
def CreateGuide (request):
	if request.method == 'POST':
		logger.info('posted')
		form = GuideForm(request.POST)
		if form.is_valid():
			logger.info('is_valid')
			g =form.save()
			# g.save()
			return HttpResponseRedirect(reverse('BuildCard', kwargs={'gslug':g.slug}))
		else:
			messages.add_message(request, messages.INFO, form.errors)
			return render_to_response("create/create_guide.html", locals(), context_instance=RequestContext(request) )
	else:
		form = GuideForm()
	return render_to_response("create/create_guide.html", locals(), context_instance=RequestContext(request) )

@login_required
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


def BuildCard (request, gslug):
	your_guide=get_object_or_404(Guide, slug=gslug)
	if your_guide.is_linear:
		s = Card(guide=your_guide)
	else:
		s = Card(guide=your_guide, is_floating_card=True)
	s.firstsave()
	return HttpResponseRedirect(reverse('EditCard', kwargs={'gslug':gslug, 'id': s.id}))

def BuildFloatingCard (request, gslug):
	s = Card(guide=get_object_or_404(Guide, slug=gslug), is_floating_card=True)
	s.firstsave()
	return HttpResponseRedirect(reverse('EditCard', kwargs={'gslug':gslug, 'id': s.id}))

@login_required
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

	#and all the cards in the guide
	all_cards = get_list_or_404(Card, guide__slug=gslug)
	c=CardResource()
	card_list = []
	# TODO REPLACE WITH GUIDE... as that works much better, and makes more sense.
	for a_card in all_cards:
		# card_list.append({'title':card.title,'resource_uri': c.get_resource_uri(card), 'id':card.id})
		if a_card.primary_media:
			card_list.append({'title':a_card.title,'resource_uri': c.get_resource_uri(a_card), 'id':a_card.id, 'primary_media':a_card.primary_media.file.thumb_url})
		else:
			card_list.append({'title':a_card.title,'resource_uri': c.get_resource_uri(a_card), 'id':a_card.id})

	all_cards_json = simplejson.dumps(card_list)

	
	#should get the guide instead, that has the relevant card info and would be more consistant TODO delete above and impliment the below
	# guide = get_object_or_404(Guide, slug=gslug)
	# g = GuideResource()
	# guide_json = g.serialize(None, g.full_dehydrate(guide), 'application/json')
	return render_to_response("create/edit_card.html", locals(), context_instance=RequestContext(request))

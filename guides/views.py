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


# Viewing Guides
# -------------------------
def GuideListView (request):
	guide_list = Guide.objects.all()
	return render_to_response("enjoy/home.html", locals(), context_instance=RequestContext(request))

def GuideDetailView (request, slug):
	guide = get_object_or_404(Guide, slug=slug)
	card_list= guide.card_set.all()
	return render_to_response("enjoy/guide_detail.html", locals(), context_instance=RequestContext(request))

def CardDetailView (request, gslug, id=None, slug=None, cnumber=None):
	if slug:
		card = get_object_or_404(Card, guide__slug=gslug, slug=slug)
	elif cnumber:
		card = get_object_or_404(Card, guide__slug=gslug, card_number=cnumber)		
	elif id:
		card = get_object_or_404(Card, id=id)
		
	media_elements = card.mediaelement_set.all()
	input_elements=card.inputelement_set.all()
	primary_media=card.primary_media
	if not card.is_floating_card:
		prev_card = card.guide.get_prev_card(card)
		next_card = card.guide.get_next_card(card)
		# logger.debug(prev_card)
		# logger.debug(next_card)
	return render_to_response("enjoy/card.html", locals(), context_instance=RequestContext(request))


def CardDetailViewByIdRedirect (request, id):
	card = get_object_or_404(Card, id=id)

	if card.slug:
		return HttpResponseRedirect(reverse('CardDetailView', kwargs={'gslug':card.guide.slug, 'slug': card.slug}))
	elif card.card_number:
		return HttpResponseRedirect(reverse('CardDetailViewByNum', kwargs={'gslug':card.guide.slug, 'cnumber': card.card_number}))
	else:
		return HttpResponseRedirect(reverse('CardDetailViewById', kwargs={'gslug':card.guide.slug, 'id': card.id}))



# Creating Guides
# -------------------------
def CreateGuide (request):
	if request.method == 'POST':
		form = GuideForm(request.POST)
		if form.is_valid():
			g =form.save()
			return HttpResponseRedirect(reverse('BuildCard', kwargs={'gslug':g.slug}))
	else:
		form = GuideForm()
	return render_to_response("create/create_guide.html", locals(), context_instance=RequestContext(request) )


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
		guide_json = g.serialize(None, g.full_dehydrate(guide), 'application/json')
	return render_to_response("create/edit_guide.html", locals(), context_instance=RequestContext(request))


def BuildCard (request, gslug):
	s = Card(guide=get_object_or_404(Guide, slug=gslug))
	s.firstsave()
	return HttpResponseRedirect(reverse('EditCard', kwargs={'gslug':gslug, 'id': s.id}))


def EditCard (request, gslug, id):
	# logger.info("---------------")
	# send the card's data as json
	s = get_object_or_404(Card, guide__slug=gslug, id=id)
	ur = CardResource()
	if not s.is_floating_card:
		prev_card = s.guide.get_prev_card(s)
		next_card = s.guide.get_next_card(s)	
	# ur_bundle = ur.build_bundle() #(obj=s, request=request) #turned out not to be neccesary
	card_json= ur.serialize(None, ur.full_dehydrate(s), 'application/json') #with newer version, full dehyrate ur_bundle
	# logger.info(card_json)
	
	mr = MediaElementResource()
	if s.primary_media is not None:
		primary_media_json = mr.serialize(None, mr.full_dehydrate(s.primary_media),'application/json' )

	#and all the cards in the guide
	all_cards = get_list_or_404(Card, guide__slug=gslug)
	c=CardResource()
	card_list = []
	for card in all_cards:
		# card_list.append({'title':card.title,'resource_uri': c.get_resource_uri(card), 'id':card.id})
		if card.primary_media:
			card_list.append({'title':card.title, 'primary_media': card.primary_media.file.thumb_url,'resource_uri': c.get_resource_uri(card), 'id':card.id})
		else:
			card_list.append({'title':card.title,'resource_uri': c.get_resource_uri(card), 'id':card.id})

	all_cards_json = simplejson.dumps(card_list)

	
	#should get the guide instead, that has the relevant card info and would be more consistant TODO delete above and impliment the below
	# guide = get_object_or_404(Guide, slug=gslug)
	# g = GuideResource()
	# guide_json = g.serialize(None, g.full_dehydrate(guide), 'application/json')
	return render_to_response("create/edit_card.html", locals(), context_instance=RequestContext(request))

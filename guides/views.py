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

# Viewing Guides
# -------------------------
def GuideListView (request):
	guide_list = Guide.objects.all()
	return render_to_response("enjoy/home.html", locals(), context_instance=RequestContext(request))

def GuideDetailView (request, slug):
	guide = get_object_or_404(Guide, slug=slug)
	card_list= guide.card_set.all()
	return render_to_response("enjoy/guide_detail.html", locals(), context_instance=RequestContext(request))

def CardDetailView (request, gslug, slug=None, cnumber=None):
	if cnumber==None:
		card = get_object_or_404(Card, guide__slug=gslug, slug=slug)
	elif slug==None:
		card = get_object_or_404(Card, guide__slug=gslug, card_number=cnumber)
	media_elements = card.mediaelement_set.all()
	input_elements=card.inputelement_set.all()
	if card.show_last_and_next_buttons:
		prev_card = card.guide.get_prev_card(card)
		next_card = card.guide.get_next_card(card)
		# logger.debug(prev_card)
		# logger.debug(next_card)
	return render_to_response("enjoy/card.html", locals(), context_instance=RequestContext(request))


def CardDetailViewById (request, id):
	card = get_object_or_404(Card, id=id)
	return HttpResponseRedirect(reverse('CardDetailView', kwargs={'gslug':card.guide.slug, 'slug': card.slug}))

	# return render_to_response("enjoy/card.html", locals(), context_instance=RequestContext(request))
	

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

from api import CardResource, SmallCardResource, GuideResource

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
	
	# send the card's data as json
	s = get_object_or_404(Card, guide__slug=gslug, id=id)
	ur = CardResource()
	# if s.guide.is_linear:
	prev_card = s.guide.get_prev_card(s)
	next_card = s.guide.get_next_card(s)	
	# ur_bundle = ur.build_bundle() #(obj=s, request=request) #turned out not to be neccesary
	card_json= ur.serialize(None, ur.full_dehydrate(s), 'application/json') #with newer version, full dehyrate ur_bundle

	#and all the cards in the guide
	all_cards = get_list_or_404(Card, guide__slug=gslug)
	c=CardResource()
	card_list = []
	for card in all_cards:
		card_list.append({'title':card.title, 'representative_media': card.representative_media,'resource_uri': c.get_resource_uri(card), 'id':card.id})
	all_cards_json = simplejson.dumps(card_list)

	#should get the guide instead, that has the relevant card info and would be more consistant TODO delete above and impliment the below
	# guide = get_object_or_404(Guide, slug=gslug)
	# g = GuideResource()
	# guide_json = g.serialize(None, g.full_dehydrate(guide), 'application/json')
	return render_to_response("create/edit_card.html", locals(), context_instance=RequestContext(request))



	# logger=getlogger()
	# logger.debug("---------------")
	# some_type_of_form =model_form_dictionary[element.__class__]

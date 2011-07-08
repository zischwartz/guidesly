# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from models import *
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime

from django.views.generic import ListView, DetailView
from forms import *
from django.core.urlresolvers import reverse

# from django.forms.models import inlineformset_factory


from django.contrib import messages
from log import getlogger

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

def CardDetailView (request, gslug, slug):
	card = get_object_or_404(Card, guide__slug=gslug, slug=slug)
	static_elements = card.staticelement_set.all()
	interactive_elements=card.interactiveelement_set.all()
	return render_to_response("enjoy/card.html", locals(), context_instance=RequestContext(request))

def CardDetailViewById (request, id):
	card = get_object_or_404(Card, id=id)
	static_elements = card.staticelement_set.all()
	interactive_elements=card.interactiveelement_set.all()
	return render_to_response("enjoy/card.html", locals(), context_instance=RequestContext(request))
	

# Creating Guides
# -------------------------
def CreateGuide (request):
	if request.user.is_authenticated():
		current_user= request.user
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
	card_list= guide.card_set.all()
	return render_to_response("create/edit_guide.html", locals(), context_instance=RequestContext(request))


def BuildCard (request, gslug):
	s = Card(guide=get_object_or_404(Guide, slug=gslug))
	s.save()
	return HttpResponseRedirect(reverse('EditCard', kwargs={'gslug':gslug, 'id': s.id}))

from api import CardResource

def EditCard (request, gslug, id):

	if request.method == 'POST':
		s= Card.objects.get(guide__slug=gslug, id=id)
		sf = CardForm(request.POST, instance=s)
		if sf.is_valid():
			savecard=sf.save(commit=False)
			savecard.brand_new=False
			savecard.save()
			if 'card_sub_add' in request.POST: #this is saving and adding a new card
				messages.info(request, "Card Saved! Here's a new card to work with.")
				return HttpResponseRedirect(reverse('BuildCard', kwargs={'gslug':gslug}))
			else:
				messages.info(request, 'Card Saved!')
				return HttpResponseRedirect(reverse('EditCard', kwargs={'gslug':gslug, 'id': s.id}))
		else:
			# return HttpResponse(sf.errors)
			return HttpResponse('that cardform did not validate, fool!')
	else:
		if request.user.is_authenticated():
			current_user= request.user
		
		
		s = get_object_or_404(Card, guide__slug=gslug, id=id)
		sf= CardForm(instance=s)
		current_static_elements = s.staticelement_set.all()
		current_interactive_elements=s.interactiveelement_set.all()
		
		static_element_form= StaticElementForm(initial={'card': s})
		static_element_form_dict= {"image":static_element_form, "video":static_element_form, "audio": static_element_form}
		
		interactive_element_form= InteractiveElementForm(initial={'card': s})
		interactive_element_form_dict = {"button": interactive_element_form, "timer":interactive_element_form}

		ur = CardResource()
		# cardr = ur.obj_get_detail( id=s.id) #request, was included
		# cardr = ur.obj_get(id=s.id)
		ur_bundle = ur.build_bundle(obj=s, request=request)
		card_json= ur.serialize(None, ur.full_dehydrate(s), 'application/json') #with newer version, full dehyrate ur_bundle
		return render_to_response("create/edit_card.html", locals(), context_instance=RequestContext(request))
		# return render_to_response("create/edit_card.html", locals(), context_instance=RequestContext(request))



def AddStaticElement (request, gslug, slug):
	s= Card.objects.get(guide__slug=gslug, slug=slug)
	if request.method == 'POST':
		form= StaticElementForm(request.POST)
		if form.is_valid():
			form.save()
			messages.info(request, "Media Added!")
			return HttpResponseRedirect(reverse('EditCard', kwargs={'gslug':gslug, 'slug': s.slug}))
		else:
			return HttpResponse(form.errors)
	else: 
		static_element_form= StaticElementForm() 
		return render_to_response("create/edit_card.html", locals(), context_instance=RequestContext(request))
	
def EditStaticElement (request, gslug, slug, elementid):
	element = StaticElement.objects.filter(card__slug=slug, id=elementid).select_subclasses()[0]
	if request.method == 'POST':
		form= StaticElementForm(request.POST, instance=element)
		if form.is_valid():
			form.save()
			messages.info(request, "Media Saved!")
			return HttpResponseRedirect(reverse('EditCard', kwargs={'gslug':gslug, 'slug': slug}))
		else:
			return HttpResponse(form.errors)
	elif request.method == 'GET':
		static_element_form= StaticElementForm(instance=element)
		return render_to_response("create/add_static.html", locals(), context_instance=RequestContext(request))
	elif request.method == 'DELETE':
		element = StaticElement.objects.get(id=elementid)
		element.delete()
		return HttpResponseRedirect(reverse('EditCard', kwargs={'gslug':gslug, 'slug': slug}))

def AddInteractiveElement(request, gslug, slug):
	s= Card.objects.get(guide__slug=gslug, slug=slug)
	if request.method == 'POST':
		form= InteractiveElementForm(request.POST)	
		if form.is_valid():
			form.save()
			messages.info(request, "Interaction Added!")
			return HttpResponseRedirect(reverse('EditCard', kwargs={'gslug':gslug, 'slug': s.slug}))
		else:
			return HttpResponse(form.errors)
	else:
		return HttpResponse(form.errors)


def EditInteractiveElement (request, gslug, slug, elementid):

	element = InteractiveElement.objects.filter(card__slug=slug, id=elementid).select_subclasses()[0]
	if request.method == 'POST':
		form= InteractiveElementForm(request.POST, instance=element)
		if form.is_valid():
			form.save()
			messages.info(request, "Interaction Saved!")
			return HttpResponseRedirect(reverse('EditCard', kwargs={'gslug':gslug, 'slug': slug}))
	elif request.method == 'GET':
		interactive_element_form= InteractiveElementForm(instance=element)
		return render_to_response("create/edit_interactive.html", locals(), context_instance=RequestContext(request))
	elif request.method == 'DELETE':
		element = InteractiveElement.objects.get(id=elementid)
		element.delete()
		return HttpResponseRedirect(reverse('EditCard', kwargs={'gslug':gslug, 'slug': slug}))
		



	# logger=getlogger()
	# logger.debug("---------------")
	# some_type_of_form =model_form_dictionary[element.__class__]

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
	slide_list= guide.slide_set.all()
	return render_to_response("enjoy/guide_detail.html", locals(), context_instance=RequestContext(request))

def SlideDetailView (request, gslug, slug):
	slide = get_object_or_404(Slide, guide__slug=gslug, slug=slug)
	static_elements = slide.staticelement_set.all()
	interactive_elements=slide.interactiveelement_set.all().select_subclasses()
	return render_to_response("enjoy/slide.html", locals(), context_instance=RequestContext(request))
	

# Creating Guides
# -------------------------
def CreateGuide (request):
	if request.user.is_authenticated():
		current_user= request.user
	if request.method == 'POST':
		form = GuideForm(request.POST)
		if form.is_valid():
			g =form.save()
			return HttpResponseRedirect(reverse('BuildSlide', kwargs={'gslug':g.slug}))
	else:
		form = GuideForm()
	return render_to_response("create/create_guide.html", locals(), context_instance=RequestContext(request) )


def EditGuide (request, gslug):
	guide = get_object_or_404(Guide, slug=gslug)
	slide_list= guide.slide_set.all()
	return render_to_response("create/edit_guide.html", locals(), context_instance=RequestContext(request))


def BuildSlide (request, gslug):
	s = Slide(guide=get_object_or_404(Guide, slug=gslug))
	s.save()
	return HttpResponseRedirect(reverse('EditSlide', kwargs={'gslug':gslug, 'slug': s.slug}))


def EditSlide (request, gslug, slug):
	if request.method == 'POST':
		s= Slide.objects.get(guide__slug=gslug, slug=slug)
		sf = SlideForm(request.POST, instance=s)
		if sf.is_valid():
			saveslide=sf.save(commit=False)
			saveslide.brand_new=False
			saveslide.save()
			if 'slide_sub_add' in request.POST: #this is saving and adding a new slide
				messages.info(request, "Slide Saved! Here's a new slide to work with.")
				return HttpResponseRedirect(reverse('BuildSlide', kwargs={'gslug':gslug}))
			else:
				messages.info(request, 'Slide Saved!')
				return HttpResponseRedirect(reverse('EditSlide', kwargs={'gslug':gslug, 'slug': s.slug}))
		else:
			# return HttpResponse(sf.errors)
			return HttpResponse('that slideform did not validate, fool!')
	else:
		s = get_object_or_404(Slide, guide__slug=gslug, slug=slug)
		sf= SlideForm(instance=s)
		current_static_elements = s.staticelement_set.all()
		current_interactive_elements=s.interactiveelement_set.all().select_subclasses()
		
		if request.user.is_authenticated():
			current_user= request.user
		# tester= available_userfiles
		static_element_form_dict = {
			'image':ImageElementForm(initial={'slide': s, 'type':'I'}),
		 	'video':VideoElementForm(initial={'slide': s, 'type':'V'}),
		 	'audio':AudioElementForm(initial={'slide': s, 'type':'A'})}
		
		# it seems this is unnecesary 
		# static_element_form_dict['image'].fields['file'].queryset=UserFile.objects.filter(owner=current_user)
		# static_element_form_dict['video'].fields['file'].queryset=UserFile.objects.filter(owner=current_user)
		# static_element_form_dict['audio'].fields['file'].queryset=UserFile.objects.filter(owner=current_user) 
		
		interactive_element_form_dict= {
			'button':InteractiveElementForm(initial={'slide': s, 'type':'B'}),
			'timer':InteractiveElementForm(initial={'slide': s, 'type':'T'})}
		
		return render_to_response("create/edit_slide.html", locals(), context_instance=RequestContext(request))



def AddStaticElement (request, gslug, slug):
	s= Slide.objects.get(guide__slug=gslug, slug=slug)
	if request.method == 'POST':
		if request.POST.__getitem__('type') =='I':
			form= ImageElementForm(request.POST, request.FILES)
		if request.POST.__getitem__('type') =='A':
			form= AudioElementForm(request.POST, request.FILES)
		if request.POST.__getitem__('type') =='V':
			form= VideoElementForm(request.POST, request.FILES)
		
		if form.is_valid():
			form.save()
			messages.info(request, "Media Added!")
			return HttpResponseRedirect(reverse('EditSlide', kwargs={'gslug':gslug, 'slug': s.slug}))
		else:
			return HttpResponse(form.errors)
	else:
		pass #this should never happen
		#static_element_form= StaticElementForm()
		return render_to_response("create/edit_slide.html", locals(), context_instance=RequestContext(request))
	
def EditStaticElement (request, gslug, slug, elementid):
	element = StaticElement.objects.filter(slide__slug=slug, id=elementid).select_subclasses()[0]
	logger=getlogger()
	logger.debug("---------------")
	some_type_of_form =model_form_dictionary[element.__class__]

	if request.method == 'POST':
		form= some_type_of_form(request.POST, request.FILES, instance=element)
		if form.is_valid():
			form.save()
			messages.info(request, "Media Saved!")
			return HttpResponseRedirect(reverse('EditSlide', kwargs={'gslug':gslug, 'slug': slug}))
	elif request.method == 'GET':
		static_element_form= some_type_of_form(instance=element)
		return render_to_response("create/add_static.html", locals(), context_instance=RequestContext(request))
	elif request.method == 'DELETE':
		element = StaticElement.objects.get(id=elementid)
		element.delete()
		return HttpResponseRedirect(reverse('EditSlide', kwargs={'gslug':gslug, 'slug': slug}))

def AddInteractiveElement(request, gslug, slug):
	s= Slide.objects.get(guide__slug=gslug, slug=slug)
	if request.method == 'POST':
		if request.POST.__getitem__('type') =='B':
			form= InteractiveElementForm(request.POST)
		if request.POST.__getitem__('type') =='T':
			form= InteractiveElementForm(request.POST)
		
		if form.is_valid():
			form.save()
			messages.info(request, "Interaction Added!")
			return HttpResponseRedirect(reverse('EditSlide', kwargs={'gslug':gslug, 'slug': s.slug}))
	else:
		pass #this shouldn't really happen


def EditInteractiveElement (request, gslug, slug, elementid):

	element = InteractiveElement.objects.filter(slide__slug=slug, id=elementid).select_subclasses()[0]
	logger=getlogger()
	logger.debug("---------------")
	some_type_of_form =model_form_dictionary[element.__class__]

	if request.method == 'POST':
		form= some_type_of_form(request.POST, instance=element)
		if form.is_valid():
			form.save()
			messages.info(request, "Interaction Saved!")
			return HttpResponseRedirect(reverse('EditSlide', kwargs={'gslug':gslug, 'slug': slug}))
	elif request.method == 'GET':
		interactive_element_form= some_type_of_form(instance=element)
		return render_to_response("create/edit_interactive.html", locals(), context_instance=RequestContext(request))
	elif request.method == 'DELETE':
		element = InteractiveElement.objects.get(id=elementid)
		element.delete()
		return HttpResponseRedirect(reverse('EditSlide', kwargs={'gslug':gslug, 'slug': slug}))
		


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


# Viewing Guides
# -------------------------
def GuideListView (request):
	guide_list = Guide.objects.all()
	return render_to_response("home.html", locals(), context_instance=RequestContext(request))

def GuideDetailView (request, slug):
	guide = get_object_or_404(Guide, slug=slug)
	slide_list= guide.slide_set.all()
	return render_to_response("guide_detail.html", locals(), context_instance=RequestContext(request))

def SlideDetailView (request, gslug, slug):
	slide = get_object_or_404(Slide, guide__slug=gslug, slug=slug)
	static_elements = slide.staticelement_set.all()
	interactive_elements=slide.interactiveelement_set.all().select_subclasses()
	return render_to_response("slide.html", locals(), context_instance=RequestContext(request))
	

# Creating Guides
# -------------------------
def CreateGuide (request):
	if request.method == 'POST':
		form = GuideForm(request.POST)
		if form.is_valid():
			g =form.save()
			# request.session['creating_guide_id'] = g.id #this was a silly way to do it
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
		static_element_form= StaticElementForm()
		return render_to_response("create/edit_slide.html", locals(), context_instance=RequestContext(request))

def AddStaticElement (request, gslug, slug):
	s= Slide.objects.get(guide__slug=gslug, slug=slug)
	static_element_form= StaticElementForm() #wtf is this doing here, remove 
	if request.method == 'POST':
		form= StaticElementForm(request.POST, request.FILES) #, instance=s)
		if form.is_valid():
			form.save()
			messages.info(request, "Media Added!")
			return HttpResponseRedirect(reverse('EditSlide', kwargs={'gslug':gslug, 'slug': s.slug}))
		else:
			return HttpResponse(form.errors)
	else:
		static_element_form= StaticElementForm()
		return render_to_response("create/edit_slide.html", locals(), context_instance=RequestContext(request))
	
def EditStaticElement (request, gslug, slug, elementid):
	# s= Slide.objects.get(guide__slug=gslug, slug=slug)
	element = StaticElement.objects.get(id=elementid)
	if request.method == 'POST':
		form= StaticElementForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.info(request, "Media Saved!")
			return HttpResponseRedirect(reverse('EditSlide', kwargs={'gslug':gslug, 'slug': slug}))
	else:
		return render_to_response("create/edit_static.html", locals(), context_instance=RequestContext(request))

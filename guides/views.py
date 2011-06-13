# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from models import *
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime

from django.views.generic import ListView, DetailView
from forms import *


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
		form = CreateGuideForm(request.POST)
		if form.is_valid():
			g =form.save()
			request.session['creating_guide_id'] = g.id
			return HttpResponseRedirect('/create/slide')
	else:
		form = CreateGuideForm()
	return render_to_response("create/create_guide.html", locals(), context_instance=RequestContext(request) )


def CreateSlide (request):
	if request.method == 'POST':
		slide_form = CreateSlideForm(request.POST)
		if slide_form.is_valid():
			s=slide_form.save(commit=False)
			s.id=request.session['creating_slide_id']
			s.save()
			return HttpResponseRedirect('/create/slide')
	else:
		creating_guide_id=request.session['creating_guide_id']
		s= Slide(guide_id=creating_guide_id)
		s.save()
		request.session['creating_slide_id'] = s.id
		slide_form = CreateSlideForm(initial={'guide':creating_guide_id})
		static_element_form= CreateStaticElementForm(initial={'slide':s.id})
	return render_to_response("create/create_slide.html", locals(), context_instance=RequestContext(request) )

def AddStaticElement (request):
	if request.method == 'POST':
		form= CreateStaticElementForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/create/slide')
	else:
		form = CreateStaticElementForm

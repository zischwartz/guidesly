from fileupload.models import UserFile
from django.views.generic import CreateView, DeleteView, ListView

from django.http import HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse

from django.conf import settings

# from guides.log import *


class UserFileCreateView(CreateView):
	model = UserFile

	def form_valid(self, form):

		f = self.request.FILES.get('file')
		file_type =  f.content_type.split('/')[0]
		self.object = form.save(commit=False)

		if file_type == 'image':
			self.object.type='image'
		elif file_type == 'audio':
			self.object.type='audio'
		elif file_type == 'video':
			self.object.type='video'
		else:
			self.objec.type='other'
		
		# logger=getlogger()
		# logger.debug(file_type)	
		# logger.debug('-----------------------------------------------------------------------------------------------------------------')
		# logger.debug("type:" + form.fields['type'])	
		# logger.debug('-----------------------------------------------------------------------------------------------------------------')
		# logger.debug(file_type)
		
		self.object.save()
		# logger.debug()	

		data = [{'name': f.name, 'url': self.object.url, 'thumbnail_url': self.object.url, 'delete_url': reverse('upload-delete', args=[f.name]), 'delete_type': "DELETE"}]
		return JSONResponse(data)

	def form_invalid (self, form):
		return HttpResponse(form.errors)


class UserFileDeleteView(DeleteView):
	model = UserFile
	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.delete()
		return JSONResponse(True)

class JSONResponse(HttpResponse):
	"""JSON response class. This does not help browsers not liking application/json."""
	def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
		content = simplejson.dumps(obj,**json_opts)
		super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)


class UserFileListView(ListView):
	context_object_name = "file_list"
	template_name = "file_list.html"
	def get_queryset(self):
		return UserFile.objects.filter(owner=self.request.user, type=self.kwargs['file_type'])
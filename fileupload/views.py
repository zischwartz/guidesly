from fileupload.models import *
from django.views.generic import CreateView, DeleteView, ListView

from django.http import HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse

from django.conf import settings
from api import UserFileResource, ImageResource

from guides.models import MediaElement, Card

from guides.log import *
logger=getlogger()

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class UserFileCreateView(CreateView):
	model = UserFile

	def form_valid(self, form):

		f = self.request.FILES.get('file')
		file_type =  f.content_type.split('/')[0]
		
		card = Card.objects.get(id=self.request.POST.get('card'))
		
		self.object = form.save(commit=False)

		if file_type == 'image':
			self.object.type='image'
			new_image=Image(original_image=self.object.file)
			new_image.save()
			self.object.image=new_image
		elif file_type == 'audio':
			self.object.type='audio'
		elif file_type == 'video':
			self.object.type='video'
		else:
			self.object.type='other'
		
		self.object.slug=f.name
		self.object.save()
		
		path = default_storage.save('/mypath', ContentFile('new content'))
		
		if file_type == 'video':
			video_sample= GetVideoSample(self.object)
			
		
		new_media_element= MediaElement(file=self.object, card=card, type=file_type) #card, owner etc needs to be passed
		
		new_media_element.save()
		#this is giving no reverse match errors. spent too much time filddling with it, stupid tastypie
		# uf = UserFileResource()
		# logger.info(self.object.pk)
		# # uri = uf.get_resource_uri(self.object)
		# # logger.info(uri)
		# uf_bundle= uf.build_bundle(obj=self.object, request=self.request)
		# logger.info(uf_bundle)
		# uf_json = uf.serialize(self.request, uf.full_dehydrate(uf_bundle), 'application/json')
		# logger.info(uf_json)
		# return(uf_json)

	
		if self.object.type=='image':
			data = [{'name': f.name, 'url': self.object.image.display_image.url, 'id': new_media_element.id, 'medium_image_url': self.object.image.medium_image.url, 'display_image_url': self.object.image.display_image.url}]
			# data = [{'name': f.name, 'url': self.object.url, 'id': self.object.id, 'medium_image_url': self.object.image.medium_image.url, 'display_image_url': self.object.image.display_image.url}]
		else:
			data = [{'name': f.name,'id': new_media_element.id, 'url': self.object.url}]
	# 		notes: using display_image.url for the url for the image. no reason to use anything bigger than the 950px one + aviary won't do well with it.
		# data = [{'name': f.name, 'url': self.object.url, 'thumbnail_url': self.object.thumb_url, 'delete_url': reverse('upload-delete', args=[f.name]), 'delete_type': "DELETE"}]
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

#unused now
class UserFileListView(ListView):
	context_object_name = "file_list"
	template_name = "file_list.html"
	def get_queryset(self):
		return UserFile.objects.filter(owner=self.request.user, type=self.kwargs['file_type'])
		
def GetVideoSample(object):
	source_url= object.url
	import subprocess
	logger.info('videosampling');
	test_url = 'http://guideslybetauserfiles.s3.amazonaws.com/userfiles/hand_1.mov'
	# ffmpeg  -itsoffset -1  -i hand.mov -vcodec mjpeg -vframes 1 -an -f rawvideo tes
	
	# subprocess.call(['ffmpeg', '-itsoffset', '-1', '-i', 'hand.mov', '-vcodec', 'mjpeg', '-vframes', '1', '-an', '-f', 'rawvideo', 'test.jpg'])
	output = subprocess.check_output(['ffmpeg', '-itsoffset', '-1', '-i', source_url, '-vcodec', 'mjpeg', '-vframes', '1', '-an', '-f', 'rawvideo', '/thumb.jpg'])
	logger.info(output)
	
	return file
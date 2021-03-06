from fileupload.models import *
from django.views.generic import CreateView, DeleteView, ListView

from django.http import HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse

from django.conf import settings
from api import UserFileResource, ImageResource, CardResource

from guides.models import MediaElement, Card

# from tastypie import get_via_uri
from api import CardResource

# from django.views.decorators.csrf import csrf_exempt


from guides.log import *
logger=getlogger()

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class UserFileCreateView(CreateView):
	model = UserFile

	# @csrf_exempt
	def form_valid(self, form):
		f = self.request.FILES.get('file')
		file_type =  f.content_type.split('/')[0]
		
		if self.request.POST.get('card'):
			# card = Card.objects.get(id=self.request.POST.get('card')) # otherwise it's coming from the general upload form
			cr = CardResource() # cardresource is imported at the end of this file
			card = cr.get_via_uri(self.request.POST.get('card'))
			#switched to uri from the id for consistency   TODO remind ben to switch it back
		else:
			card = None
			
		self.object = form.save(commit=False)

		if file_type == 'image':
			self.object.type='image'
			try:
				new_image=Image(original_image=self.object.file)
				new_image.save()
				self.object.image=new_image
			except:
				pass
		elif file_type == 'audio':
			self.object.type='audio'
		elif file_type == 'video':
			self.object.type='video'
			try:
				video_sample_url= GetVideoSample(self.object, self.request.user.username, f.name.split('.')[0])
				new_image=Image(original_image=video_sample_url)
				self.object.image=new_image
			except:
				pass
		else:
			self.object.type='other'
			file_type = 'other'
		
		self.object.slug=f.name
		self.object.save()
		
		#we're uploading from a card editing page
		if card:
			new_media_element= MediaElement(file=self.object, card=card, type=file_type) #card, owner etc needs to be passed
			new_media_element.save()
			relevant_id = new_media_element.id
		else:
			relevant_id= self.object.id
		
		# data = [{'name': f.name, 'url': self.object.ur.display_image.url, 'id': relevant_id, 'medium_image_url': self.object.image.medium_image.url, 'display_image_url': self.object.image.display_image.url}]
		
		
		if self.object.type=='image':
			data = [{'name': f.name, 'url': self.object.url, 'id': relevant_id, 'medium_image_url': self.object.image.medium_image.url, 'display_image_url': self.object.image.display_image.url}]
			# notes: using display_image.url for the url for the image. no reason to use anything bigger than the 950px one + aviary won't do well with it.
		# elif self.object.type=='video':
			# data = [{'name': f.name, 'url': self.object.url, 'id': relevant_id, 'medium_image_url': self.object.image.medium_image.url, 'display_image_url': self.object.image.display_image.url}]
		else:
			data = [{'name': f.name,'id': relevant_id, 'url': self.object.url}]
			


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


import subprocess
from django.conf import settings

def GetVideoSample(object, user_name, file_name):
	source_url= object.url
	logger.info('videosampling:%s' % source_url);
	# test_url = 'http://guideslybetauserfiles.s3.amazonaws.com/userfiles/hand_1.mov'
	# output = subprocess.check_output(['ffmpeg', '-itsoffset', '-1', '-i', source_url, '-vcodec', 'mjpeg', '-vframes', '1', '-an', '-f', 'rawvideo', '-'])

	pre_path = 'vidthumbs/' + user_name +  '/' + file_name + '.jpg'
	logger.info(pre_path)

	# ffmpeg  -itsoffset -1  -i hand.mov -vcodec mjpeg -vframes 1 -an -f rawvideo tes
	# subprocess.call(['ffmpeg', '-itsoffset', '-1', '-i', 'hand.mov', '-vcodec', 'mjpeg', '-vframes', '1', '-an', '-f', 'rawvideo', 'test.jpg'])

	# works
	# output = subprocess.check_output(['ffmpeg', '-itsoffset', '-1', '-i', source_url, '-vcodec', 'mjpeg', '-vframes', '1', '-an', '-f', 'rawvideo', '-'])
	output = subprocess.check_output(['ffmpeg', '-ss', '-1', '-i', source_url, '-vcodec', 'mjpeg', '-vframes', '1', '-an', '-f', 'rawvideo', '-'])
	
	post_path = default_storage.save(pre_path, ContentFile(output))
	# logger.info(post_path)
	# logger.info('done uploading and getting thumbnail of a video')
	
	return (settings.MEDIA_URL + post_path)
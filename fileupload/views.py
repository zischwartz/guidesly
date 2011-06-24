from fileupload.models import UserFile
from django.views.generic import CreateView, DeleteView

from django.http import HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse

from django.conf import settings

class UserFileCreateView(CreateView):
    model = UserFile

    def form_valid(self, form):
        self.object = form.save()
        f = self.request.FILES.get('file')
        data = [{'name': f.name, 'url': self.object.url, 'thumbnail_url': self.object.url, 'delete_url': reverse('upload-delete', args=[f.name]), 'delete_type': "DELETE"}]
        return JSONResponse(data)

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

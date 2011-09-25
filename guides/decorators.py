# from functools import wraps
from django.shortcuts import  get_object_or_404
from models import Guide
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden


def require_owner(func):
    def inner(request, gslug, *args, **kwargs):
	#id=None, ? for card...add eventually
        guide = get_object_or_404(Guide, slug=gslug)
        if guide.owner != request.user:
            return HttpResponseForbidden(
                "You are not the owner of this guide!"
            )
        else:
            return func(request, gslug, *args, **kwargs)
    return inner


def require_published_and_public(func):
    def inner(request, gslug, *args, **kwargs):
        guide = get_object_or_404(Guide, slug=gslug)
		
        # first, is it your guide?
        if  guide.owner == request.user:
            return func(request, gslug, *args, **kwargs)
		
        # next, is it not published yet, or private?
        if not guide.published or guide.private:
            return HttpResponseForbidden(
                "Not published, not public, or doesn't exist")
        else:
            return func(request, gslug, *args, **kwargs)
    return inner



# 
# 
# def owner_required(Model=None):
#     """
#     Usage:
# 
#     @permission_required('blogs.change_entry')
#     @owner_required(Entry)
#     def manage_entry(request, object_id=None, object=None):
# 
#     @permission_required('blogs.delete_entry')
#     @owner_required()
#     def entry_delete(*args, **kwargs):
#         kwargs["post_delete_redirect"] = reverse('manage_blogs')
#         return delete_object(*args, **kwargs)
#     """
#     def _decorator(viewfunc):
#         def _closure(request, *args, **kwargs):
#             user = request.user
#             grant = False
#             model = Model
#             mod_edit = False
#             if 'object_id' in kwargs:
#                 object_id = int(kwargs['object_id'])
#                 if model:
#                     mod_edit = True
#                 elif 'model' in kwargs:
#                     model = kwargs['model']
#                 object = get_object_or_404(model, pk=object_id)
# 
#                 if user.is_superuser:
#                     grant = True
#                 else:
#                     if user.__class__ == model:
#                         grant = object_id == user.id
#                     else:
#                         names = [rel.get_accessor_name() for rel in user._meta.get_all_related_objects() if rel.model == model]
#                         if names:
#                             grant = object_id in [o.id for o in eval('user.%s.all()' % names[0])]
#                             # grant = object_id in [o.id for o in eval('user.%s.all()' % names[0])]
#                 if not grant:
#                     response = render_to_response("403.html", {'object': object}, context_instance=RequestContext(request))
#                     response.status_code = 403
#                     return response
#                 if mod_edit:
#                     kwargs['object'] = object
# 
#             response = viewfunc(request, *args, **kwargs)
#             return response
# 
#         return wraps(viewfunc)(_closure)
#     return _decorator
from tastypie.resources import ModelResource

from guides.models import StaticElement

from model_utils.managers import InheritanceManager


class StaticElementResource(ModelResource):
	class Meta:
		queryset= StaticElement.objects.all()


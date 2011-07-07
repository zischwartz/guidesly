from models import *
from django.contrib import admin


class GuideAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}

class StaticElementInline (admin.TabularInline):
	model=StaticElement
	extra=1


class MultipleChoiceInquiryInline (admin.TabularInline):
	model=MultipleChoiceInquiry
	extra=1

class InteractiveElementInline (admin.TabularInline):
	model=InteractiveElement
	extra=1


class CardAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}
	inlines = [StaticElementInline, InteractiveElementInline, MultipleChoiceInquiryInline]


admin.site.register(Guide, GuideAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(StaticElement)
# admin.site.register(ImageElement)
admin.site.register(InteractiveElement)
# admin.site.register(MultipleChoice)
# admin.site.register(MultipleChoiceInquiry)
admin.site.register(Action)
admin.site.register(ConditionalAction)
# admin.site.register(YNInquiry)
# admin.site.register(NValueInquiry)
# admin.site.register(TValueInquiry)
# admin.site.register(Timer)

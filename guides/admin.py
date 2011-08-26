from models import *
from django.contrib import admin


class GuideAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}

class MediaElementInline (admin.TabularInline):
	model=MediaElement
	extra=1


# class MultipleChoiceInquiryInline (admin.TabularInline):
# 	model=MultipleChoiceInquiry
# 	extra=1

class InputElementInline (admin.TabularInline):
	model=InputElement
	fk_name = 'card'
	extra=1


class CardAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}
	inlines = [MediaElementInline, InputElementInline,]# MultipleChoiceInquiryInline]


admin.site.register(Guide, GuideAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(MediaElement)
# admin.site.register(ImageElement)
admin.site.register(InputElement)
# admin.site.register(MultipleChoice)
# admin.site.register(MultipleChoiceInquiry)
admin.site.register(Theme)
admin.site.register(Action)
admin.site.register(MapElement)
admin.site.register(MapPointElement)

admin.site.register(ConditionalAction)
# admin.site.register(YNInquiry)
# admin.site.register(NValueInquiry)
# admin.site.register(TValueInquiry)


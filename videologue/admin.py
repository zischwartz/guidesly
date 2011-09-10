from django.contrib import admin
from videologue.models import Gallery, GalleryUpload, Video, ConvertVideo

try:
    from batchadmin.admin import BatchModelAdmin
except ImportError:
    BatchModelAdmin = admin.ModelAdmin


class GalleryAdmin(BatchModelAdmin):
    batch_actions = ['delete_selected']
    list_display = ('title', 'date_added', 'video_count', 'is_public')
    list_filter = ['date_added', 'is_public']
    date_hierarchy = 'date_added'
    prepopulated_fields = {'title_slug': ('title',)}
    filter_horizontal = ('videos',)


class VideoAdmin(BatchModelAdmin):
    batch_actions = ['delete_selected']
    list_display = ('title', 'date_taken', 'date_added', 'is_public', 'tags', 'view_count', 'flv_video', 'admin_thumbnail')
    list_filter = ['date_added', 'is_public']
    list_per_page = 10
    prepopulated_fields = {'title_slug': ('title',)}
    exclude = ('image', 'flv_video', 'mp4_video', 'ogv_video')


class ConvertVideoAdmin(BatchModelAdmin):
    batch_actions = ['delete_selected']
    list_display = ('video', 'started', 'error')


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(GalleryUpload)
admin.site.register(Video, VideoAdmin)
admin.site.register(ConvertVideo, ConvertVideoAdmin)

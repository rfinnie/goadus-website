from django.contrib import admin

from .models import Image, ImageFile, ImageSet


class ImageAdmin(admin.ModelAdmin):
    list_display = ('slug', 'content_type', 'original_filename', 'date_added', 'user')
    ordering = ('-image_set__date_added',)
    search_fields = ('slug', 'original_filename')

    def date_added(self, obj):
        return obj.image_set.date_added
    date_added.short_description = 'Date Added'
    date_added.admin_order_field = 'image_set__date_added'

    def user(self, obj):
        return obj.image_set.user
    user.short_description = 'User'
    user.admin_order_field = 'image_set__user'


class ImageFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'original_filename', 'type', 'date_added')
    ordering = ('-image__image_set__date_added',)
    search_fields = ('file',)

    def original_filename(self, obj):
        return obj.image.original_filename
    original_filename.short_description = 'Original Filename'
    original_filename.admin_order_field = 'image__original_filename'

    def date_added(self, obj):
        return obj.image.image_set.date_added
    date_added.short_description = 'Date Added'
    date_added.admin_order_field = 'image__image_set__date_added'


class ImageSetAdmin(admin.ModelAdmin):
    list_display = ('slug', 'date_added', 'date_expires', 'user')
    ordering = ('-date_added',)
    search_fields = ('slug',)


admin.site.register(Image, ImageAdmin)
admin.site.register(ImageFile, ImageFileAdmin)
admin.site.register(ImageSet, ImageSetAdmin)

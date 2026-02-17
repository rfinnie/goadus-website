# SPDX-PackageName: goadus-website
# SPDX-PackageSupplier: Ryan Finnie <ryan@finnie.org>
# SPDX-PackageDownloadLocation: https://github.com/finnix/goadus-website
# SPDX-FileCopyrightText: © 2020 Ryan Finnie <ryan@finnie.org>
# SPDX-License-Identifier: MPL-2.0

from django.contrib import admin

from .models import ApiKey, Image, ImageFile, ImageSet


class CustomModelAdmin(admin.ModelAdmin):
    change_form_template = "admin/custom_change_form.html"

    def render_change_form(self, request, context, *args, **kwargs):
        # Build a list of related children objects and their counts
        # so they may be linked to in the admin interface
        related_links = []
        if "object_id" in context and hasattr(self.model._meta, "get_fields"):
            related_objs = [
                f for f in self.model._meta.get_fields() if (f.one_to_many or f.one_to_one) and f.auto_created and not f.concrete
            ]
            for obj in related_objs:
                count = obj.related_model.objects.filter(**{obj.field.name: context["object_id"]}).count()
                if count > 0:
                    related_links.append((obj, obj.related_model._meta, count))
        context.update({"related_links": related_links})

        return super(CustomModelAdmin, self).render_change_form(request, context, *args, **kwargs)


class ImageAdmin(CustomModelAdmin):
    list_display = ("slug", "content_type", "original_filename", "date_added", "user")
    ordering = ("-image_set__date_added",)
    search_fields = ("slug", "original_filename")

    def date_added(self, obj):
        return obj.image_set.date_added

    date_added.short_description = "Date Added"
    date_added.admin_order_field = "image_set__date_added"

    def user(self, obj):
        return obj.image_set.user

    user.short_description = "User"
    user.admin_order_field = "image_set__user"


class ImageFileAdmin(CustomModelAdmin):
    list_display = ("id", "file", "original_filename", "type", "date_added")
    ordering = ("-image__image_set__date_added",)
    search_fields = ("file",)

    def original_filename(self, obj):
        return obj.image.original_filename

    original_filename.short_description = "Original Filename"
    original_filename.admin_order_field = "image__original_filename"

    def date_added(self, obj):
        return obj.image.image_set.date_added

    date_added.short_description = "Date Added"
    date_added.admin_order_field = "image__image_set__date_added"


class ImageSetAdmin(CustomModelAdmin):
    list_display = ("slug", "date_added", "date_expires", "user")
    ordering = ("-date_added",)
    search_fields = ("slug",)


class ApiKeyAdmin(CustomModelAdmin):
    list_display = ("slug", "date_added", "date_expires", "user")
    ordering = ("-date_added",)
    search_fields = ("slug",)


admin.site.register(Image, ImageAdmin)
admin.site.register(ImageFile, ImageFileAdmin)
admin.site.register(ImageSet, ImageSetAdmin)
admin.site.register(ApiKey, ApiKeyAdmin)

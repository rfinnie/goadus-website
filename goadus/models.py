import os
import uuid

from django.conf import settings
from django.core.files import storage
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone

from .utils import werder_api_key, werder_name


class IGoadStorage(storage.FileSystemStorage):
    def url(self, name):
        return storage.FileSystemStorage.url(self, os.path.split(name)[-1])


class ImageSet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=False, null=False)
    slug = models.SlugField(default=werder_name, unique=True, blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)
    date_added = models.DateTimeField(default=timezone.now, blank=False, null=False)
    date_expires = models.DateTimeField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse_lazy("imageset", kwargs={"slug": self.slug})

    def __str__(self):
        return self.slug


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=False, null=False)
    slug = models.SlugField(default=werder_name, unique=True, blank=False, null=False)
    original_filename = models.CharField(max_length=200, blank=False, null=False)
    content_type = models.CharField(max_length=200, blank=True, null=True)
    image_set = models.ForeignKey(ImageSet, on_delete=models.CASCADE, blank=False, null=False)

    def get_absolute_url(self):
        return reverse_lazy("image", kwargs={"slug": self.slug})

    def __str__(self):
        return self.slug


class ImageFile(models.Model):
    TYPES = (
        ("uploaded", "Unsanitized original image"),
        ("original", "Original image"),
        ("medium", "Resized image"),
        ("thumbnail", "Thumbnail image"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=False, null=False)
    file = models.ImageField(max_length=200, storage=IGoadStorage(), blank=False, null=False)
    type = models.CharField(max_length=200, choices=TYPES, blank=False, null=False)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return os.path.split(self.file.name)[-1]


class ApiKey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=False, null=False)
    slug = models.SlugField(default=werder_api_key, unique=True, blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)
    date_added = models.DateTimeField(default=timezone.now, blank=False, null=False)
    date_expires = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.slug

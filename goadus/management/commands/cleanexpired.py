import os

from django.core.management.base import BaseCommand
from django.utils import timezone

from goadus.models import ApiKey, ImageSet


class Command(BaseCommand):
    help = "Clean expired objects"

    def handle(self, *args, **options):
        for image_set in ImageSet.objects.filter(date_expires__lt=timezone.now()):
            for image in image_set.image_set.all():
                for image_file in image.imagefile_set.all():
                    os.remove(image_file.file.path)
            image_set.delete()

        for api_key in ApiKey.objects.filter(date_expires__lt=timezone.now()):
            api_key.delete()

import os

from django.core.management.base import BaseCommand
from django.utils import timezone

from goadus.models import ApiKey, ImageSet
from goadus.settings import MEDIA_ROOT


class Command(BaseCommand):
    help = "Clean expired objects"

    def make_segmented_path(self, fn):
        return "{}/{}/{}".format(fn[0:1], fn[1:2], fn)

    def handle(self, *args, **options):
        for image_set in ImageSet.objects.filter(date_expires__lt=timezone.now()):
            for image in image_set.image_set.all():
                for image_file in image.imagefile_set.all():
                    os.remove(
                        "{}/{}".format(
                            MEDIA_ROOT, self.make_segmented_path(image_file.file.name)
                        )
                    )
            image_set.delete()

        for api_key in ApiKey.objects.filter(date_expires__lt=timezone.now()):
            api_key.delete()

from datetime import timedelta
import io
import json
import mimetypes
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File as DjangoFile
from django.core.files.images import ImageFile as DjangoImageFile
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView
import PIL.ExifTags
import PIL.Image

from .forms import UploadForm
from .models import ApiKey, Image, ImageFile, ImageSet
from .utils import werder_name


def process_image(image):
    image_format = image.format
    orientation_tag = {v: k for k, v in PIL.ExifTags.TAGS.items()}["Orientation"]
    try:
        orientation = image.getexif()[orientation_tag]
    except KeyError:
        orientation = 1

    # TODO: Handle uncommon rotations
    # https://www.impulseadventure.com/photo/exif-orientation.html
    if orientation == 3:
        image = image.rotate(180, expand=True)
    elif orientation == 6:
        image = image.rotate(270, expand=True)
    elif orientation == 8:
        image = image.rotate(90, expand=True)
    else:
        # Strips exif at the same time
        image = image.rotate(0, expand=True)

    image.format = image_format
    return image


def handle_uploaded_file(fileobj, image_set, noresize=False):
    original_filename = fileobj.name
    content_type = None
    extension = None
    django_file = DjangoFile

    try:
        pil_image = process_image(PIL.Image.open(fileobj))
    except OSError:
        # OSError: cannot identify image file '/not/an/image'
        pil_image = None
    pil_map = {"GIF": ("image/gif", ".gif"), "JPEG": ("image/jpeg", ".jpg"), "PNG": ("image/png", ".png")}
    if pil_image:
        if pil_image.format in pil_map:
            content_type = pil_map[pil_image.format][0]
            extension = pil_map[pil_image.format][1]
            django_file = DjangoImageFile
        else:
            pil_image.close()
            pil_image = None
    else:
        content_type = mimetypes.guess_type(original_filename)[0]

    if extension is None:
        extension = "." + os.path.splitext(original_filename)[-1][1:]

    image = Image()
    image.original_filename = original_filename
    image.content_type = content_type
    image.image_set = image_set
    image.save()

    raw_converted_file = django_file(fileobj)
    raw_converted_file.file.seek(0)
    image_file = ImageFile()
    raw_converted_file.name = "{}{}".format(werder_name(), extension)
    image_file.file = raw_converted_file
    image_file.type = "uploaded"
    image_file.image = image
    image_file.save()

    if pil_image is None or pil_image.format in ("GIF",):
        # Exact same as "uploaded"
        raw_converted_file = django_file(fileobj)
        raw_converted_file.file.seek(0)
        image_file = ImageFile()
        raw_converted_file.name = "{}{}".format(werder_name(), extension)
        image_file.file = raw_converted_file
        image_file.type = "original"
        image_file.image = image
        image_file.save()
    else:
        # Rotate if needed, strip EXIF
        raw_converted_file = django_file(io.BytesIO())
        pil_image.save(raw_converted_file.file, pil_image.format)
        raw_converted_file.file.seek(0)
        image_file = ImageFile()
        raw_converted_file.name = "{}{}".format(werder_name(), extension)
        image_file.file = raw_converted_file
        image_file.type = "original"
        image_file.image = image
        image_file.save()
        raw_converted_file.close()

    if pil_image is None or noresize:
        return image

    if pil_image.width > 1280 or pil_image.height > 1280:
        pil_image.thumbnail((1280, 1280), PIL.Image.LANCZOS)

        raw_converted_file = django_file(io.BytesIO())
        pil_image.save(raw_converted_file.file, pil_image.format)
        raw_converted_file.file.seek(0)
        image_file = ImageFile()
        raw_converted_file.name = "{}{}".format(werder_name(), extension)
        image_file.file = raw_converted_file
        image_file.type = "medium"
        image_file.image = image
        image_file.save()
        raw_converted_file.close()

    if pil_image.width > 200 or pil_image.height > 200:
        pil_image.thumbnail((200, 200), PIL.Image.LANCZOS)

    raw_converted_file = django_file(io.BytesIO())
    pil_image.save(raw_converted_file.file, pil_image.format)
    raw_converted_file.file.seek(0)
    image_file = ImageFile()
    raw_converted_file.name = "{}{}".format(werder_name(), extension)
    image_file.file = raw_converted_file
    image_file.type = "thumbnail"
    image_file.image = image
    image_file.save()
    raw_converted_file.close()

    pil_image.close()
    fileobj.close()
    return image


class UploadView(LoginRequiredMixin, FormView):
    form_class = UploadForm
    template_name = "goadus/upload.html"

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if not form.is_valid():
            return self.form_invalid(form)
        image_set = ImageSet()
        image_set.user = request.user
        if form.cleaned_data["temporary"]:
            image_set.date_expires = timezone.now() + timedelta(days=7)
        image_set.save()
        for fileobj in request.FILES.getlist("files"):
            handle_uploaded_file(fileobj, image_set, form.cleaned_data["noresize"])
        return HttpResponseRedirect(reverse_lazy("imageset", kwargs={"slug": image_set.slug}))


class ImageView(generic.DetailView):
    template_name = "goadus/image.html"
    model = Image


class ImageSetView(generic.DetailView):
    template_name = "goadus/imageset.html"
    model = ImageSet


@csrf_exempt
def api_upload(request):
    try:
        api_key = ApiKey.objects.get(slug=request.POST.get("key", None))
    except ApiKey.DoesNotExist:
        return HttpResponseForbidden()
    user = api_key.user
    if "noresize" in request.POST and request.POST["noresize"]:
        noresize = True
    else:
        noresize = False
    image_set = ImageSet()
    image_set.user = user
    if "temporary" in request.POST and request.POST["temporary"]:
        image_set.date_expires = timezone.now() + timedelta(days=7)
    image_set.save()
    images = {}
    for fileobj in request.FILES.getlist("files"):
        image = handle_uploaded_file(fileobj, image_set, noresize)
        images[image.slug] = {
            "url": request.build_absolute_uri(str(reverse_lazy("image", kwargs={"slug": image.slug}))),
            "imagefiles": {},
        }
        for imagefile in image.imagefile_set.all():
            if imagefile.type == "uploaded":
                continue
            images[image.slug]["imagefiles"][imagefile.type] = {
                "width": imagefile.file.width,
                "height": imagefile.file.height,
                "size": imagefile.file.size,
                "url": imagefile.file.url,
            }

    out = {
        "imagesets": {
            image_set.slug: {
                "url": request.build_absolute_uri(str(reverse_lazy("imageset", kwargs={"slug": image_set.slug}))),
                "images": images,
            }
        }
    }
    return HttpResponse(json.dumps(out), content_type="application/json")


def index(request):
    template = loader.get_template("goadus/index.html")
    return HttpResponse(template.render({}, request))

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms


class MultipleFileInput(forms.ClearableFileInput):
    # https://docs.djangoproject.com/en/4.2/topics/http/file-uploads/#uploading-multiple-files
    allow_multiple_selected = True
    # https://stackoverflow.com/questions/61535301/files-not-uploaded-in-django-form-encoding-type-incorrect
    needs_multipart_form = True


class MultipleFileField(forms.FileField):
    # https://docs.djangoproject.com/en/4.2/topics/http/file-uploads/#uploading-multiple-files
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={"multiple": True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class UploadForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super(UploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Upload"))

    files = MultipleFileField()
    temporary = forms.BooleanField(required=False, label="Delete after about a week")
    noresize = forms.BooleanField(required=False, label="Do not resize")

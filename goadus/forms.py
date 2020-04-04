from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms


class UploadForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Upload', css_class='btn btn-primary btn-lg btn-block'))

    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    temporary = forms.BooleanField(required=False, label='Delete after about a week')
    noresize = forms.BooleanField(required=False, label='Do not resize')

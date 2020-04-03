from django import forms


class UploadForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    temporary = forms.BooleanField(required=False)
    noresize = forms.BooleanField(required=False)

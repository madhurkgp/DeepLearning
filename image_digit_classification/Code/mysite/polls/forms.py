from django import forms
from .models import InputImagesNew

class ImageForm(forms.ModelForm):
    class Meta:
        model = InputImagesNew
        fields = ('image_name', 'file')

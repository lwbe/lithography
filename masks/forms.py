from django import forms
 
from .models import Image,Mask
 

class UploadMaskForm(forms.ModelForm):
    class Meta:
        model  = Mask
        fields = '__all__'


class UploadImageForm(forms.ModelForm):     
    class Meta:
        model = Image
        fields = ['image']

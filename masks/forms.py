from django import forms


from django.forms.models import inlineformset_factory

from .models import Motif,Mask,Image

class MotifTypeDataForm(forms.Form):
    rank = forms.IntegerField(
        label="Rank",
        widget=forms.TextInput(attrs={'placeholder':'rank',
                                      'class':'form-control',
                                      'readonly':'true'})
    )
    name_of_field = forms.CharField(
        label="Name of the field",
        widget=forms.TextInput(attrs={'class':'form-control',
                                      'placeholder':'Name of the field',
                                      'required':'true'}))

class MotifTypeForm(forms.Form):
    name = forms.CharField(label="Motif type name",
                           widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Motif type name'}),
                           help_text="Enter a name")
    nb_parameters = forms.IntegerField(label="Number of parameters",
                           widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Number of parameters'}))

class MotifModelForm(forms.ModelForm):

    class Meta:
        model = Motif
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super(MotifModelForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'placeholder':f,
                                      'class':'form-control'})


class MaskModelForm(forms.ModelForm):
    image=forms.ImageField(widget=forms.ClearableFileInput(attrs={
                           'multiple':""}))

    class Meta:
        model = Mask
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'placeholder':f,
                                      'class':'form-control'})


class ImageModelForm(forms.ModelForm):
    class Meta:
        model = Image
        fields=('image','mask')
from django import forms
from .models import Motif, Mask, Image, MotifType

from django.utils.translation import ugettext_lazy as _

# ---
class MotifTypeDataForm(forms.Form):
    rank = forms.IntegerField(
        label="Rank",
        widget=forms.TextInput(attrs={'placeholder': 'rank',
                                      'class': 'form-control',
                                      'readonly': 'true'})
    )
    name_of_field = forms.CharField(
        label="Name of the field",
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Name of the field',
                                      'required': 'true'}))

# ---
class MotifTypeForm(forms.Form):
    name = forms.CharField(label="Motif type name",
                           widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Motif type name'}),
                           help_text="Enter a name")

    nb_parameters = forms.IntegerField(label="Number of parameters",
                                       widget=forms.TextInput(attrs={
                                           'class': 'form-control',
                                           'placeholder': 'Number of parameters'}))


# ---
class MotifModelForm(forms.ModelForm):

    class Meta:
        model = Motif
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MotifModelForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({
                'placeholder': f,
                'class':'form-control'})

# ---
class MaskModelForm(forms.ModelForm):
    image=forms.ImageField(widget=forms.ClearableFileInput(attrs={
                           'multiple': ""}))

    class Meta:
        model = Mask
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({
               'placeholder' : f,
               'class' : 'form-control'
            })

# ---
class ImageModelForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', 'mask')

# ---
class MaskMotifSearchForm(forms.ModelForm):
    type = forms.ModelChoiceField(label=_("Motif Type"),
                                  queryset=MotifType.objects.all())
    value_0 = forms.CharField(label=_("First parameter"))
    value_1 = forms.CharField(label=_("Second parameter"))
    value_2 = forms.CharField(label=_("Third parameter"))
    value_3 = forms.CharField(label=_("Fourth parameter"))
    value_4 = forms.CharField(label=_("Fifth parameter"))
    value_5 = forms.CharField(label=_("Sixth parameter"))
    value_6 = forms.CharField(label=_("Seventh parameter"))
    value_7 = forms.CharField(label=_("Eighth parameter"))
    value_8 = forms.CharField(label=_("Nineth parameter"))
    value_9 = forms.CharField(label=_("Tenth parameter"))
    condition = forms.ChoiceField(label=_("Condition"),
                                  choices=[('---',_('Select'))]+list(Mask.conditionChoices))

    field_order = ['type',
                   'value_0',
                   'value_1',
                   'value_2',
                   'value_3',
                   'value_4',
                   'value_5',
                   'value_6',
                   'value_7',
                   'value_8',
                   'value_9',
                   'name',
                   'usage',
                   'localisation',
                   'manufacturer',
                   'conceptor',
                   'level',
                   'creationYear',
                   'condition',
                   'polarisation',
                   'description',
                   'area']

    class Meta:
        model = Mask
        fields = ['name',
                  'usage',
                  'localisation',
                  'manufacturer',
                  'conceptor',
                  'level',
                  'creationYear',
                  'polarisation',
                  'description',
                  'area']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            if f in ['level','creationYear','description','area']:
                self.fields[f].widget = forms.TextInput()
                self.fields[f].initial = ''

            self.fields[f].widget.attrs.update({
                'placeholder': f,
                'class':'form-control'})
            self.fields[f].required = False


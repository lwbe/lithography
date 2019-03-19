from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.forms import formset_factory
from django.urls import reverse,reverse_lazy
from django.utils.http import urlencode


import json

from django.views.generic import ListView,CreateView,View,DetailView,UpdateView

# Create your views here.
from .models import MotifType,Motif,Mask,Image,Usage,Localisation,Manufacturer
from .forms import MotifTypeForm,MotifTypeDataForm,MotifModelForm,MaskModelForm,ImageModelForm

from django.http import JsonResponse
#----------------------------------------------------------------------------------
# Image class stuff
#----------------------------------------------------------------------------------


class imageCUView(View):
    success_url = reverse_lazy('listmask')

    def get(self, request):
        self.request.session['mask_id']=self.request.GET['mask_id']
        images_list = Image.objects.filter(mask_id=self.request.session['mask_id'])
        return render(self.request, 'first/image_cu.html', {'images': images_list})

    def post(self, request):
        # if we press submit then we return success URL
        print(request.POST,"imagetodelete" in request.POST)
        if 'submit' in request.POST:
            # we check if there are images to delete
            if "imagetodelete" in request.POST:
                
                for i in request.POST.getlist("imagetodelete"):
                    
                    Image.objects.get(id=i).delete()

            
            return HttpResponseRedirect(self.success_url)

        # otherwise we create the image

        form = ImageModelForm({'mask':self.request.session['mask_id']},
                              self.request.FILES)
        if form.is_valid():
            image = form.save()
            print(image,image.image.name,image.id)
            data = {'is_valid': True, 'name': image.image.name, 'url': image.image.url, 'id':image.id}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

#----------------------------------------------------------------------------------
# Mask class stuff
#----------------------------------------------------------------------------------


class maskListView(ListView):
    model = Mask

    def get_queryset(self):
        if 'field' in self.kwargs:
            field=self.kwargs['field']
            fieldId=self.kwargs['fieldid']
            print(field,fieldId)
            return Mask.objects.filter(**{field:fieldId})
        else:
            return super().get_queryset()

class maskDetailView(DetailView):
    model = Mask
    context_object_name='mask'

class maskCUView(UpdateView):
    model = Mask
    fields='__all__'
    template_name = 'mask_cu.html'
    success_url = reverse_lazy('listmask')

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None

    def form_valid(self, form):
        print('form is valid')
        self.object = form.save()
        # if we click add image we need to send the id of the mask created
        if 'addimage'in self.request.POST:
            get_maskid = urlencode({'mask_id':self.object.id})
            self.success_url='%s?%s' % (reverse('createimage'),get_maskid)

        return HttpResponseRedirect(self.get_success_url())



def maskSearchView(request):
    return HttpResponseRedirect(reverse('listmask'))

# ----------------------------------------------------------------------------------
# Usage class stuff
# ----------------------------------------------------------------------------------
class usageListView(ListView):
    model = Usage

class usageCUView(UpdateView):
    model = Usage
    fields ='__all__'
    template_name = 'usage_cu.html'
    success_url = reverse_lazy('listusage')

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None

# ----------------------------------------------------------------------------------
# Localisation class stuff
# ----------------------------------------------------------------------------------
class localisationListView(ListView):
    model = Localisation

class localisationCUView(UpdateView):
    model = Localisation
    fields ='__all__'
    template_name = 'localisation_cu.html'
    success_url = reverse_lazy('listlocalisation')

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None

# ----------------------------------------------------------------------------------
# Manufacturer class stuff
# ----------------------------------------------------------------------------------
class manufacturerListView(ListView):
    model = Manufacturer

class manufacturerCUView(UpdateView):
    model =Manufacturer
    fields ='__all__'
    template_name = 'manufacturer_cu.html'
    success_url = reverse_lazy('listmanufacturer')

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None


# ----------------------------------------------------------------------------------
# Motif class stuff
# ----------------------------------------------------------------------------------
class motifListView(ListView):
    model = Motif

class motifCUView(UpdateView):
    model = Motif
    form_class = MotifModelForm
    #    fields ='__all__'
    template_name = 'motif_cu.html'
    success_url = reverse_lazy('listmotif')

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None

    # creating a method like this makes it available in template
    # with the {{ view.motiftype_def }}
    # see https://reinout.vanrees.org/weblog/2014/05/19/context.html
    # This function sends a json objects containing information about the select

    def motiftype_def(self):

        all_m={}
        for i in list(MotifType.objects.values()):
            m={'nb_params': i['nb_parameters']}
            l=[]
            for j in json.loads(i['parameters_data']):
                l.append(j['name_of_field'])
            m.update({'params':l})
            all_m.update({'val%d'%i['id'] : m})

        return json.dumps(all_m)

#----------------------------------------------------------------------------------
# MotifType class stuff
#----------------------------------------------------------------------------------
class motifTypeListView(ListView):
    model = MotifType

def motifTypeCUView(request,pk_motif=None):

    MotifTypeDataFormSet = formset_factory(MotifTypeDataForm, extra=0)
    UPDATE=False
    if pk_motif:
        # we update
        UPDATE=True
        motif_object = get_object_or_404(MotifType, id=pk_motif)
        form = MotifTypeForm(initial={'name': motif_object.name,
                                      'nb_parameters': motif_object.nb_parameters,
                                      'step':motif_object.step})

        formset_data = json.loads(motif_object.parameters_data)
        formset = MotifTypeDataFormSet(initial=formset_data)
    else:
        form = MotifTypeForm()
        formset = MotifTypeDataFormSet()

    # we deal with the incoming data
    if request.method == 'POST':

        form = MotifTypeForm(request.POST)
        formset = MotifTypeDataFormSet(request.POST,request.FILES)

        IS_VALID=True
        if form.is_valid():
            data_to_save = form.cleaned_data
            if formset.is_valid():
                data_to_save.update({'parameters_data':json.dumps(formset.cleaned_data)})
            else:
                IS_VALID=False
        else:
            IS_VALID=False


        if IS_VALID:
            if UPDATE:
                name=motif_object.name
            else:
                name=form.cleaned_data['name']
            m,created = MotifType.objects.update_or_create(name=name,defaults=data_to_save)

            return HttpResponseRedirect(reverse('listmotiftype'))

    return render(request,'motiftype_cu.html',
                  {'form':form,
                   'formset':formset,
                   'update':UPDATE})

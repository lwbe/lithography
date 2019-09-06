from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
import json

from django.views.generic import ListView, View, DetailView, UpdateView, FormView

# Create your views here.
from .models import MotifType, Motif, Mask, Image, Usage, Localisation, Manufacturer
from .forms import MaskMotifSearchForm, ImageModelForm

from django.http import JsonResponse

#----------------------------------------------------------------------------------
# class to make a generic class based view
#----------------------------------------------------------------------------------
class genericCreateUpdateView(UpdateView):
    template_name = 'generic_cu.html'
    fields ='__all__'

    # redefining getobject makes the create and update possible in one class
    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        if 'type' in context:
            context['isdetail'] = True

        # adding some value to the context
        m = self.model

        context['title'] = "%s form" % m._meta.verbose_name_plural.capitalize()
        return context

class genericListView(ListView):
    template_name = "generic_list.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        # adding some value to the context
        m = self.model

        context['title']  = m._meta.verbose_name_plural.capitalize()
        context['model']  = m._meta.verbose_name
        # fields should be set in the model by a function called
        # get_available_fields
        fields = m.get_available_fields()

        fnames = [m._meta.get_field(f.split('__')[0]).verbose_name for f in fields]

        context['fields'] = fnames
        context['datas'] = self.get_queryset().values_list(*fields)

        if self.model == Mask:
            context['broken_masks'] = [i[0] for i in m.objects.filter(condition="broken").values_list("id")]
        else:
            context['broken_masks'] = []

        context['update_url'] = "update%s" % m._meta.verbose_name.replace(' ','')
        context['detail_url'] = "detail%s" % m._meta.verbose_name.replace(' ','')
        return context

#----------------------------------------------------------------------------------
# Image class stuff
#----------------------------------------------------------------------------------


class imageCUView(View):
    success_url = reverse_lazy('listmask')

    def get(self, request):
        self.request.session['mask_id']=self.request.GET['mask_id']
        images_list = Image.objects.filter(mask_id=self.request.session['mask_id'])
        return render(self.request, 'masks/image_cu.html', {'images': images_list})

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

class maskListView(genericListView):
    model = Mask

    def get_queryset(self):
        if 'field' in self.kwargs:
            field=self.kwargs['field']
            fieldId=self.kwargs['fieldid']
            if field == 'motif':
                field='motifs'
            elif field == 'motif type':
                field='motifs__type'
            print(field,fieldId)
            return Mask.objects.filter(**{field:fieldId}).values()
        else:
            return super().get_queryset()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        # adding some value to the context
        m = self.model

        context['title']  = m._meta.verbose_name_plural.capitalize()
        context['model']  = m._meta.verbose_name
        # fields should be set in the model by a function called
        # get_available_fields
        fields = m.get_available_fields()

        fnames = [m._meta.get_field(f.split('__')[0]).verbose_name for f in fields]

        context['fields'] = fnames
        #context['datas'] = \
        values_list = self.get_queryset().values_list(*fields)
        l = []

        if values_list:
            cur_list = list(values_list[0])
            cur_index = cur_list[0]

            index_m2m = [fnames.index('motifs')]

            for i in values_list[1:]:
                if i[0] != cur_index:
                    l.append(cur_list)
                    cur_list = list(i)
                    cur_index = i[0]
                else:
                    for j in index_m2m:
                        cur_list[j] +=", "+ i[j]
            # we add the last element
            l.append(cur_list)

        context['datas'] = l
        context['update_url'] = "update%s" % m._meta.verbose_name.replace(' ','')
        context['detail_url'] = "detail%s" % m._meta.verbose_name.replace(' ','')
        return context

class maskDetailView(DetailView):
    model = Mask
    context_object_name='mask'

class maskCUView(genericCreateUpdateView):
    model = Mask
    template_name = 'mask_cu.html'
    success_url = reverse_lazy('listmask')

    def form_valid(self, form):
        print('form is valid')
        self.object = form.save()
        # if we click add image we need to send the id of the mask created
        if 'addimage'in self.request.POST:
            get_maskid = urlencode({'mask_id':self.object.id})
            self.success_url='%s?%s' % (reverse('createimage'),get_maskid)

        return HttpResponseRedirect(self.get_success_url())


#---
class maskSearchView(FormView):
    template_name = "mask_search.html"
    form_class = MaskMotifSearchForm

    def motiftype_def(self):

        all_m = {}
        for m in MotifType.objects.all().values():
            all_m.update({
                m['name']:
                    {
                    'nb'   : m['nb_parameters'] ,
                    'names' : [v for k,v in m.items() if k.startswith("param_name") and v]
                    }
            })
        return json.dumps(all_m)


from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
def tofloat(v):
    try:
        return float(v)
    except:
        return None
        raise ValidationError(
             _('Invalid value: %(value)s'),
              code='invalid',
            params={'value': v},
            )
# --- utility function to extract a range from a string of the type
# a:b   -> a  , b
# a     -> a  , ''    # might be a only?
# a:    -> a  , ''
# :b    -> '' , b

def getBounds(v):
    if not ":" in v:
        return tofloat(v),

    l,u = v.split(":")
    return tofloat(l),tofloat(u)

# ---
class maskResultSearchView(maskListView):

    def get_queryset(self):
        # here we are called from the form maskSearchView and we have some parameters
        # through the get.
        get_parameters = [k for k in self.request.GET.keys()]
        query_parameters = {}
        for k in get_parameters:
            v = self.request.GET[k]
            if v:
                if k.startswith("value"):
                    b = getBounds(v)
                    if len(b) == 1:
                        query_parameters.update({"motifs__%s" % k: b[0]})
                    else:
                        l,u = b
                        if l:
                            query_parameters.update({"motifs__%s__gte" % k: l})
                        if u:
                            query_parameters.update({"motifs__%s__lte"%k : u})

                elif k == "type":
                    query_parameters.update({"motifs__type__id" : v})
                elif k in ["name" , "description" , "level"]:
                    query_parameters.update({"%s__contains" % k : v})
                elif k in ['usage','manufacturer']:
                    query_parameters.update({"usage" : v})
                elif k in ['condition','polarisation']:
                    if v != '---':
                        query_parameters.update({"%s" % k : v})
        return Mask.objects.filter(**query_parameters).values()



# ----------------------------------------------------------------------------------
# Usage class stuff
# ----------------------------------------------------------------------------------
class usageListView(genericListView):
    model = Usage

class usageCUView(genericCreateUpdateView):
    model = Usage
    success_url = reverse_lazy('listusage')

# ----------------------------------------------------------------------------------
# Localisation class stuff
# ----------------------------------------------------------------------------------
class localisationListView(genericListView):
    model = Localisation

class localisationCUView(genericCreateUpdateView):
    model = Localisation
    success_url = reverse_lazy('listlocalisation')

# ----------------------------------------------------------------------------------
# Manufacturer class stuff
# ----------------------------------------------------------------------------------
class manufacturerListView(genericListView):
    model = Manufacturer

class manufacturerCUView(genericCreateUpdateView):
    model =Manufacturer
    success_url = reverse_lazy('listmanufacturer')

# ----------------------------------------------------------------------------------
# Motif class stuff
# ----------------------------------------------------------------------------------
class motifListView(genericListView):
    model = Motif

class motifCUView(genericCreateUpdateView):
    model = Motif
    success_url = reverse_lazy('listmotif')

    # creating a method like this makes it available in template
    # with the {{ view.motiftype_def }}
    # see https://reinout.vanrees.org/weblog/2014/05/19/context.html
    # This function sends a json objects containing information about the select

    def motiftype_def(self):

        all_m={}
        for m in MotifType.objects.all().values():
            all_m.update({
                m['name']:
                    {
                    'nb'   : m['nb_parameters'] ,
                    'names' : [v for k,v in m.items() if k.startswith("param_name") and v]
                    }
            })
        return json.dumps(all_m)

#----------------------------------------------------------------------------------
# MotifType class stuff
#----------------------------------------------------------------------------------
class motifTypeListView(genericListView):
    template_name = "motiftype_list.html"
    model = MotifType

class motifTypeCUView(genericCreateUpdateView):
    model = MotifType
    success_url = reverse_lazy('listmotiftype')


from django.http import HttpResponse
import datetime

def info(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

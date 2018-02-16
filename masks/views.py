from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

 
from .forms import UploadImageForm,UploadMaskForm
from .models import Image,Mask
 
from django.shortcuts import render

# Create your views here.
# a simple test page
from django.http import HttpResponse

def home(request):
    return HttpResponse('Hello World')

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class MaskCreate(CreateView):
    template_name = 'masks/mask_create.html'
    
    form_class          = UploadMaskForm
    
    

class MaskUpdate(UpdateView):
    template_name= 'index.html'


def uploadfile(request):
    if request.method == 'POST':
        maskform = UploadImageForm(request.POST, request.FILES)
        imageform = UploadImageForm(request.POST, request.FILES)
        if maskform.is_valid() and imageform.is_valid():
            newmask=maskform.save()
            new_file = Image(file = request.FILES['file'],mask=newmask)
            new_file.save()
 
            return HttpResponseRedirect(reverse('masks:home'))
    else:
        maskform = UploadImageForm(request.POST, request.FILES)
        imageform = UploadImageForm(request.POST, request.FILES)

 
    data = {'mform': maskform,
            'iform':imageform}
    return render(request,'masks/index.html', data) # , context_instance=RequestContext(request))

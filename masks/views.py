from django.shortcuts import render

# Create your views here.
# a simple test page
from django.http import HttpResponse

def home(request):
    return HttpResponse('Hello World')

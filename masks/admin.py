from django.contrib import admin

# Register your models here.
from .models import Mask,Image,About

admin.site.register(Mask)
admin.site.register(Image)
admin.site.register(About)

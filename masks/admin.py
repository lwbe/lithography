from django.contrib import admin

# Register your models here.
from .models import Mask, Image, About, Motif, MotifType

admin.site.register(Mask)
admin.site.register(Motif)
admin.site.register(MotifType)
admin.site.register(Image)
admin.site.register(About)

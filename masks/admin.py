from django.contrib import admin

# Register your models here.
from .models import Mask,Image

# this will expose all the fields in the model

#==============================================================
#admin.site.register(Mask)
#==============================================================
# is equal to 
#==============================================================
# to make a selection of the field.
#class MaskAdmin(admin.ModelAdmin):
#    pass
#admin.site.register(Mask,MaskAdmin)
#==============================================================
# but using the MaskAdmin will be usefull for customisation

# mask
class MaskAdmin(admin.ModelAdmin):
    pass

admin.site.register(Mask,MaskAdmin)

# image
class ImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Image,ImageAdmin)

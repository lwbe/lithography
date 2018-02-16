from django.contrib import admin

# Register your models here.
from .models import Motifs, MotifsTypes,Fabricants,Masques,Usages,Localisations,Image

class UsagesAdmin(admin.ModelAdmin):
   list_display   = ('nom',)

class LocalisationsAdmin(admin.ModelAdmin):
   list_display   = ('nom',)

class FabricantsAdmin(admin.ModelAdmin):
   list_display   = ('id','rais_soc')
   
class MotifsAdmin(admin.ModelAdmin):
   list_display   = ('typemotif','dim1','dim2','dim3','dim4','pas')
   

class MotifsTypesAdmin(admin.ModelAdmin):
   list_display   = ('nom',)
   
class ImageInline(admin.StackedInline):
    model           = Image
    extra=1
 
    
class MasquesAdmin(admin.ModelAdmin):
   list_display   = ('num','nom','usage','concepteur','fabricant','local','anneecre')
   inlines = [ ImageInline]
 
#class ImageAdmin(admin.ModelAdmin):
   #list_display   = ('masque','image')
#   inlines = [ ImageInline, ]

admin.site.register(Motifs,MotifsAdmin)
admin.site.register(MotifsTypes,MotifsTypesAdmin)
admin.site.register(Fabricants,FabricantsAdmin)
admin.site.register(Masques,MasquesAdmin)
admin.site.register(Usages,UsagesAdmin)
admin.site.register(Localisations,LocalisationsAdmin)
admin.site.register(Image)
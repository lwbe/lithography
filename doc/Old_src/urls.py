"""gestionC2N URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url


from . import views

urlpatterns = [
        url(r'^home/', views.searchMasques , name = 'home'), 
        #  Fabricants **************
        url(r'^fabricants/', views.fabricants , name = 'fabricants'), 
        url(r'^createfabricant/$', views.createupdatefabricant , name = 'createfabricant'), 
        url(r'^updatefabricant/(?P<id>[0-9]+)/$', views.createupdatefabricant , name = 'updatefabricant'),        
        #  Usages ********************
        url(r'^usages/', views.usages , name = 'usages'),
        url(r'^createusage/$', views.createupdateusage , name = 'createusage'), 
        url(r'^updateusage/(?P<id>[0-9]+)/$', views.createupdateusage , name = 'updateusage'),  
        url(r'^masquesparusage/(?P<id>[0-9]+)/$', views.masquesparusage , name = 'masquesparusage'),
        
        #  Motifs ********************
        url(r'^motifs/', views.motifs, name = 'motifs'), 
        url(r'^createmotif/$', views.createmotif , name = 'createmotif'), 
        url(r'^updatemotif/(?P<id>[0-9]+)/$', views.updatemotif , name = 'updatemotif'), 
        #  Types motifs ********************
        url(r'^typemotif/', views.typemotif , name = 'typemotif'),
        url(r'^createtypemotif/$', views.createupdatetypemotif , name = 'createtypemotif'), 
        url(r'^updatetypemotif/(?P<id>[0-9]+)/$', views.createupdatetypemotif , name = 'updatetypemotif'),          
        #  Masques ********************
        url(r'^masques/', views.masques , name = 'masques'), 
        url(r'^detailsmasque/(?P<id>[0-9]+)/$', views.detailsmasque , name = 'detailsmasque'),
        url(r'^masquesparmotif/(?P<id>[0-9]+)/$', views.masquesparmotif , name = 'masquesparmotif'),
        
        url(r'^createmasque/$', views.createupdatemasque , name = 'createmasque'), 
        url(r'^updatemasque/(?P<id>[0-9]+)/$', views.createupdatemasque , name = 'updatemasque'),    
        
        #  Localisations ********************
        url(r'^localisations/', views.localisations , name = 'localisations'),
        url(r'^createlocalisation/$', views.createupdatelocalisation , name = 'createlocalisation'), 
        url(r'^updatelocalisation/(?P<id>[0-9]+)/$', views.createupdatelocalisation , name = 'updatelocalisation'), 
        url(r'^masquesparusage/(?P<id>[0-9]+)/$', views.masquesparusage , name = 'masquesparusage'),
        url(r'^masquesparlocal/(?P<id>[0-9]+)/$', views.masquesparlocal , name = 'masquesparlocal'),
                       
        
        # Images
        url(r'^help/', views.help , name = 'help'),
        url(r'^imagesmasque/(?P<id>[0-9]+)/$', views.imagesmasque , name = 'imagesmasque'),
        url(r'^zoomimage1/(?P<id>[0-9]+)/$', views.zoomimage1 , name = 'zoomimage1'),
        url(r'^zoomimage2/(?P<id>[0-9]+)/$', views.zoomimage2 , name = 'zoomimage2'),
		
        #connexion
        url(r'^connexion/', views.connexion , name = 'connexion'),
        url(r'^deconnexion/', views.deconnexion , name = 'deconnexion'),
        
]

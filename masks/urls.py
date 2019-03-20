from django.urls import path,include
from django.contrib.auth.decorators import login_required, permission_required
from . import views

urlpatterns = [

    # account stuff
    path('accounts/', include('django.contrib.auth.urls')),

    path('motiftypes',
         views.motifTypeListView.as_view(),
         name='listmotiftype'),
    path('motiftype/create',
         #login_required(views.motifTypeCUView),
         login_required(views.motifTypeCUView.as_view()),
         name='createmotiftype'),
    path('motiftype/update/<int:pk>/',
         #login_required(views.motifTypeCUView),
         login_required(views.motifTypeCUView.as_view()),
         name='updatemotiftype'),
    path('motiftype/detail/<int:pk>/',
         views.motifTypeCUView.as_view(extra_context={'type':'detail'}),
         name='detailmotiftype'),

    path('motifs',
         views.motifListView.as_view(),
         name='listmotif'),
    path('motif/create',
         login_required(views.motifCUView.as_view()),
         name='createmotif'),
    path('motif/update/<int:pk>/',
         login_required(views.motifCUView.as_view()),
         name='updatemotif'),
    path('motif/detail/<int:pk>/',
         views.motifCUView.as_view(extra_context={'type':'detail'}),
         name='detailmotif'),

    path('usages',
         views.usageListView.as_view(),
         name='listusage'),
    path('usage/create',
         login_required(views.usageCUView.as_view()),
         name='createusage'),
    path('usage/update/<int:pk>/',
         login_required(views.usageCUView.as_view()),
         name='updateusage'),

    path('localisation',
         views.localisationListView.as_view(),
         name='listlocalisation'),
    path('localisation/create',
         login_required(views.localisationCUView.as_view()),
         name='createlocalisation'),
    path('localisation/update/<int:pk>/',
         login_required(views.localisationCUView.as_view()),
         name='updatelocalisation'),

    path('manufacturer',
         views.manufacturerListView.as_view(),
         name='listmanufacturer'),
    path('manufacturer/create',
         login_required(views.manufacturerCUView.as_view()),
         name='createmanufacturer'),
    path('manufacturer/update/<int:pk>/',
         login_required(views.manufacturerCUView.as_view()),
         name='updatemanufacturer'),

    path('masks',
         views.maskListView.as_view(),
         name='listmask'),
    path('masks/<field>/<int:fieldid>',
         views.maskListView.as_view(),
         name='listmaskwithfield'),
    path('mask/create',
         login_required(views.maskCUView.as_view()),
         name='createmask'),
    path('mask/update/<int:pk>/',
         login_required(views.maskCUView.as_view()),
         name='updatemask'),
    path('mask/detail/<int:pk>/',
         views.maskDetailView.as_view(),
         name='detailmask'),

    path('mask/search',
         views.maskSearchView,
         name='searchmask'),

    path('image/create',
         login_required(views.imageCUView.as_view()),
         name='createimage'),

]


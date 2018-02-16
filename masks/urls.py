from django.conf.urls import url,include

from masks import views as masks_views
  
urlpatterns = [
    # the home page
    url(r'^$', masks_views.uploadfile, name='uploadfile'),


    # 
    url(r'^create$', masks_views.MaskCreate.as_view(), name='create'),
    
]

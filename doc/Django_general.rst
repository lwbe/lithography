================
Notes sur django
================

Note d'installation de django pour l'application des masques. Une notice pour le deploiement sera faite ailleurs. J'ai utilisé comme réference

- https://simpleisbetterthancomplex.com/series/2017/09/04/a-complete-beginners-guide-to-django-part-1.html
- https://openclassrooms.com/courses/developpez-votre-site-web-avec-le-framework-django/le-fonctionnement-de-django


Note le cour d'openclassroom est pour la version 2.0 de django. Il faut certainement faire un choix rapidement pour ne pas perdre les infos déjà contenues dans la base. 

Installation
============
on installe django dans un environement virtuel python 3.6 (compilé à la main) et django==1.11. Note pour python il faut installer tk-dev et bzip2 libbz2-dev mais si ce n'est pas du tout necessaire pour django

.. code-block:: bash
		
  /usr/local/bin/python3 -m venv .virtualenv/python3_django
  . .virtualenv/python3_django/bin/activate
  pip install django==1.11

On va installer d'autre paquet au fur et à mesure mais on peut commencer par installer pillow et rst2pdf car on va avoir besoin de pillow pour traiter les images dans django et rst2pdf pour transformer cette doc en pdf.

.. code-block:: bash

  pip install pillow rst2pdf

On oublie de faire des **pip freeze** pour voir les paquets necessaire pour l'application. Il faut donner ce fichier avec les sources et donc dans le repertoire du projet on crée un sous repertoire utils qui contient ce fichier.

Création de l'application
=========================
On se place dans un repertoire de travvail ici **~/Devel/Python/Django** qui nous servira a retrouver nos petits

.. code-block:: bash
		
cd Devel/Python/
mkdir Django
cd Django/

demarrage
---------
On crée un projet **lithography** puis l'application **masks**. Une des difficultés de django sur des petits projet et cette notion de projet et d'application parcequ'en general le projet est une application. 

.. code-block:: bash
		
  django-admin startproject lithography
  cd lithography # on se retrouve dans le repertoire contenant manage.py
  django-admin startapp masks

On modifie en suite **settings.py** qui se trouve dans **\~/Devel/Python/Django/lithography/lithography** ou on rahoute:

.. code-block:: python

   'masks', 

dans la liste **INSTALLED_APPS**.

On rajoute aussi

.. code-block:: python

   MEDIA_URL = '/media/'
   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

pour pouvoir gerer les fichiers et image que l'on televersera sur le site. Attention il faut créer le repertoire associé.

premier test
------------
On rajoute des données dans deux fichiers

Dans views.py on rajoute:

.. code-block:: python
		
   from django.http import HttpResponse

   def home(request):
       return HttpResponse('Hello World')

et dans urls.py on rajoute

.. code-block:: python

  # import for masks
  from masks import views
  urlpatterns = [                        #  <------ligne deja presente
    url(r'^$',views.home,name='home'),
    url(r'^admin/', admin.site.urls),    #  <------ligne deja presente
  ]                                      #  <------ligne deja presente

Pour le test on lance manage.py avec la commande runserver mais il se plaint

.. code-block:: python
  
    You have 13 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.    
    Run 'python manage.py migrate' to apply them.

On pointe un navigateur vers http://localhost:8000/ et on voit bien le **hello world** de la vue.

Ce qui nous amène à la fin du premier test

Questions à résoudre:

- passage en django 2.0?
- mettre ce code sous github et comment le deployer (pip install?) bien détaillé la différence entre l'utilisation de git pour le développement et pour le deploiement avec le setup.py qui va bien.


second test (models)
--------------------
On va créer des modèles pour définir les infos que l'on veut pour les masques. On commence petit car on veut surtout voir comment utiliser jQuery File Upload (https://github.com/blueimp/jQuery-File-Upload).

Dans le fichier **models.py** on met:

.. code-block:: python
  from django.db import models

  from django.utils.translation import ugettext_lazy as _
  # Create your models here.

  class Mask(models.Model):
    name   = models.CharField(_("Nom"),max_length=100,default='')
    number = models.IntegerField(_("Numero"),default=1)
    
    
    def __str__(self):
        return self.number
  
  class Image(models.Model):
    mask = models.ForeignKey(Mask)
    image  = models.ImageField(_("Image"),default='',blank=True,null=True,upload_to="images/")
         
    def __unicode__(self):
         return self.mask.number

    def __str__(self):
        return self.mask.number

puis pour prendre en compte ce fichier ont fait:

.. code-block:: bash

   python ./manage.py migrate
   python ./manage.py makemigrations
   python ./manage.py migrate

Pour pouvoir acceder aux modèles via le site d'admin de django il

creer un compte surperutilisateur
+++++++++++++++++++++++++++++++++

.. code-block:: bash
   python ./manage.py createsuperuser

ou on donne un login un email et un mot de pass

et rajouter dans le fichier **masks/admin.py**
++++++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: python
		
  from django.contrib import admin
  
  # Register your models here.
  from .models import Mask,Image
    
  
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

Voir https://docs.djangoproject.com/fr/1.11/ref/contrib/admin/ pour les parametres de la page admin qui sont très nombreux. 

On peut alors ensuite se connecter sur le site localhost:8000/admin et rentrer son login mot de passe. 
  
Ensuite on devrait faire la mise en production via uwsgi et nginx.

uwsgi et nginx
--------------
Voir la doc de deployement.
  
Utilisation de jquery-file-upload
---------------------------------
Nous allons maintenant regarder comment utiliser un plugin jquery, jquery-file-upload pour televerser des images à partir d'une page. Ensuite nous verrons comment faire un modéle pour les masques qui permette d'utiliser ce plugin.

Je suis https://simpleisbetterthancomplex.com/tutorial/2016/11/22/django-multiple-file-upload-using-ajax.html

On ajoute:

..code-block:: python

  from django.conf import settings
  from django.conf.urls.static import static
  if settings.DEBUG:
      urlpatterns += static(settings.Medi_URL,document_root=settings.MEDIA_ROOT)

Dans le fichier *lithography/urls.py*


templates
---------
Dans le repertoire de masks on crée un repertoire templates/masks/ dans lequel on mettra les htmls.




Internationnalisation
---------------------
Voir la doc officielle de django mais aussi https://openclassrooms.com/courses/developpez-votre-site-web-avec-le-framework-django/l-internationalisation-1


Il faut verifier que la variable  soit mise à True dans le fichier **lithography/settings.py'USE_I18N = True

Dans les modèles il faut utiliser ugettext_lazy pour que l'évaluation se fasse au run time et non a l'initialisation car on contraindrai la chaine au démarrage de l'application.
from django.utils.translation import ugettext_lazy as _

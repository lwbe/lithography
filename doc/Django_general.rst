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

dans la liste **INSTALLED_APPS.

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

 Fin du premier test

 Questions à résoudre:

- passage en django 2.0?
- mettre ce code sous github et comment le deployer (pip install?) bien détaillé la différence entre l'utilisation de git pour le développement et pour le deploiement avec le setup.py qui va bien.

  

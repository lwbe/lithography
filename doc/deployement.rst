=================================
Deploiement de django uwsgi+nginx
=================================

La doc suivie est http://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html

installation de uwsgi
---------------------
On commence par installer uwsgi par:

.. code-block:: bash

  pip install uwsgi


On verifie que l'application marche avec **manage.py** par

.. code-block:: bash

  python ./manage.py runserver

Et des que cela marche on peut tester uwsgi par:

.. code-block:: bash

  uwsgi --http :8000 --module lithography.wsgi

Remarques:

- on lance cette commande dans l'environement virtuel et donc on a accès à tout les modules
- l'argument de uwsgi **lithography.wsgi** est composé du répertoire ici lithography dans lequel se trouve un fichier wsgi.py.
- enfin si on se trompe dans le nom du module on a un message d'erreur **Internal Server Error** 

Le fichier wsgi.py contient

.. code-block:: python
 
  """
  WSGI config for lithography project.
  
  It exposes the WSGI callable as a module-level variable named ``application``. 
  
  For more information on this file, see
  https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
  """
  
  import os
  
  from django.core.wsgi import get_wsgi_application  
  
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lithography.settings") 
  
  application = get_wsgi_application()
  
Installation de nginx
---------------------
J'installe sur une debian stretch nginx par **apt install nginx-full** et on verifie en allant sur http://localhost
qu'on a bien une page indiquant que nginx est up.

Les fichiers de configuration de nginx sont dans **/etc/site-available** et ils sont affichés si un lien pointe vers eux dans **sites-enabled**

On crée le site **/etc/nginx/sites-available/lithography.conf** qui contient.

.. code-block:: bash
		
  # lithography.conf

  # the upstream component nginx needs to connect to
  upstream django {
      # server unix:///path/to/your/mysite/mysite.sock; # for a file socket
      server 127.0.0.1:8001; # for a web port socket (we'll use this first)
  }

  # configuration of the server
  server {
      # the port your site will be served on
      listen      8000;
      # the domain name it will serve for
      server_name .example.com; # substitute your machine's IP address or FQDN
      charset     utf-8;

      # max upload size
      client_max_body_size 75M;   # adjust to taste

      # Django media
      location /media  {
          alias /path/to/your/mysite/media;  # your Django project's media files - amend as required
      }

      location /static {
          alias /path/to/your/mysite/static; # your Django project's static files - amend as required
      }

      # Finally, send all non-media requests to the Django server.
      location / {
          uwsgi_pass  django;
          include     /path/to/your/mysite/uwsgi_params; # the uwsgi_params file you installed
      }
  }
  

 Remarques

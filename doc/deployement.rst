===========
Deployement
===========


Doc to deploy the app to a new machine

Base install
============
This is a simple way to install the software. In case you know what you are doing you can do as you please.

Here I will install the app and use nginx + uwsgi to serve it.

In a home directory I will create a directory called **lithography**.

Then I will create a directory inside called **nginx_conf", create a virtual env and clone the repository:

.. code-block:: bash

  cd
  mkdir lithography
  cd litography
  mkdir nginx_conf

  # clone the repository
  git clone https://github.com/lwbe/lithography.git    # this will create a directory called lithography and
                                                       # yes the path will be lithography/lithography


  # virtual env
  python3.5 -m venv venv  # this will create a directory venv
  source venv/bin/activate

  # to fill the virtual env
  pip install -r lithography/utils/requirements.txt

Note to install the requirements you might need to install python3.5-dev (in debian)

Then you need to create the database

.. code-block:: bash

   # setting some env vars to make it work for now they will be set in the nginx configuration file
   export DJANGO_SECRET_KEY="a secret key not important for now"
   export DJANGO_DEBUG=False
   export DJANGO_ALLOWED_HOST=HOST_FQDN  # set your machine FQDN here

   cd lithography # in fact you should be in the directory where manage.py is
   ./manage.py makemigrations
   ./manage.py migrate



In the case of C2N there is a file to import the data from the previous version to run. It will be of course a one time use. This file is in utils and called initialize_from_olddb and you should set the original db and the directory for the images

Now we can set the http server

uwsgi+nginx
===========

uwsgi is already installed since it is in the requirements.txt


To test uwsgi

.. code-block:: bash

    uwsgi --chdir=~/lithography_test/lithography/
          --module=lithography.wsgi:application
          --env DJANGO_SETTINGS_MODULE=lithography.settings
          --env DJANGO_SECRET_KEY='YOUR_SECRET_KEY'
          --env DJANGO_DEBUG=False
          --env DJANGO_ALLOWED_HOST=YOUR_HOST_FQDN
          --master
          --pidfile=/tmp/project-master.pid
          --socket=127.0.0.1:49152
          --processes=5
          --http :8123

**NOTE: THIS SHOULD BE ON  ONE LINE**

Then you can check if it works in going to http://YOUR_HOST_FQDN:8123

the name is set via the env var DJANGO_ALLOWED_HOST and the port via the http swith of the uwsgi command.


nginx
-----
I will only talk about the configuration of nginx for the app website.




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

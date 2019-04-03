=====
Todos
=====


Things to keep in mind not ordered for now:

- code

  - clean the source tree (remove old source code, unused javascript and old docs)
  - get the javascript library to make the code stand alone (remove CDN)
  - internationalisation

- system

  - reorganize the folder on the server to get production and test website
  - set the correct uwsgi daemon with vassals
  - use https and decide the certificates to use (let's encrypt because of the automatice renewal or terena)

- website pages

  - create the info page to summarize stats (and to dump the site?)
  - create the search page.
  - edit the about page to create a doc.




Some notes
==========

Translation is a work in progress for now and doesn't work

Translation
+++++++++++
To translate a text the following operations should be performed

- prepare django for translation
- write the text using one of ugettext, ngettext, pgettext or their _lazy equivalent
- generate the .po file for the language using django-admin makemessage
- modify the .po file to write the translated sentences.

Below I will briefly explain how it works but for a more complete explanation see
https://docs.djangoproject.com/fr/2.1/topics/i18n/translation/

A tutorial is given at https://phraseapp.com/blog/posts/quick-guide-django-i18n/


preparation
-----------
The settings.py file should contain

.. code-block:: python

   LANGUAGE_CODE = 'en-us'
   TIME_ZONE = 'UTC'
   USE_I18N = True
   USE_L10N = True
   USE_TZ = True

in the root directory you need a folder called **locale**

In the lithography app the idea is not to get a on-the-fly localised site but more
a site that can be set in different languages once for all. The idea is to have french
words but in case this software become popular ;) it could be easily localised.

To localise the site one just need to set the **LANGUAGE_CODE** variable in
**settings.py** for example:


.. code-block:: python

   LANGUAGE_CODE = 'fr'


writing the strings to be translated
------------------------------------
The translated text can be set in python code but also in the template files.

For the templates file, one need to write the text with the **{% trans  %}** tag.
For example

.. code-block:: html

   {% load i18n %}

   <h1>{% trans 'WelcomeHeading' %}</h1>


Note the need of the **{% load i18 %}**.

The translation of the name of the variable is done through the use of

.. code-block:: python

    from django.utils.translation import ugettext_lazy as _


and when a variable has to be translated one has to write

.. code-block:: python

    a = _("Usage")


instead of

.. code-block:: python

   a = "Usage"

for example

.. code-block:: python

    name = models.CharField(_("Usage"), max_length=100)


To help the translation, in giving some extra information one can use the comments
formatted in a special way.

.. code-block:: python

  def my_view(request):
    # Translators: This message appears on the home page only
    output = gettext("Welcome to my site.")

The information will be found in the .po file which will contain the translation in the following structure.

.. code-block:: python

   #. Translators: This message appears on the home page only
   # path/to/python/file.py:123
   msgid "Welcome to my site."
   msgstr ""


create the .po file
-------------------

.. code-block:: python




translation and use
-------------------




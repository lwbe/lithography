==================
some useful stuff
==================


templates
---------
https://docs.djangoproject.com/en/2.1/ref/templates/api/#compiling-a-string


Here is a simple way to check templates with a dictionnary from the shell

.. code-block:: python

   from django.template import Template,Context
   template = Template("My name is {{ my_name }}.")

In the above url the test is done with

.. code-block:: python

   context = Context({"my_name": "Adrian"})
   template.render(context)


For a more complex case

.. code-block:: python

   fields = Mask.get_available_fields()
   fnames = [Mask._meta.get_field(f.split('__')[0]).verbose_name for f in fields]
   context={}
   context['fields'] = fnames
   context['datas'] = Mask.objects.all().values(*fields)

   ct = Context(context)

   template = Template("""{% for data in datas %}
            <tr>
                {% for k,v in data.items %}
                <td>
                  {{ v }}
                </td>
                {% endfor %}
            </tr>
            {% endfor %}""")

   print(template.render(ct))


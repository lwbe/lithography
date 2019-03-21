import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crispyCBVm2m.settings")
django.setup()
from django.template.loader import get_template


template=get_template('first/generic.html')
print(template.render({'model' : 'world',
                       'fields': ['id','name'],
                       'datas' : [['1','test1'],['2','test2']]}
                      ))

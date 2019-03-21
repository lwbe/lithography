import os,django

from django.db.models import Q

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crispyCBVm2m.settings")
django.setup()

from first.models import Mask,Motif,MotifType,Manufacturer,Localisation,Usage
import json

#remove all the data
MotifType.objects.all().delete()
Motif.objects.all().delete()
Mask.objects.all().delete()
Manufacturer.objects.all().delete()
Localisation.objects.all().delete()
Usage.objects.all().delete()


Usage.objects.create(name='TBH')
Usage.objects.create(name='TLM')

Localisation.objects.create(localisation='shelf 1')
Localisation.objects.create(localisation='shelf 2')


Manufacturer.objects.create(corporateName='mask maker')


# creating some MotifType
data = {'name':'square',
    'nb_parameters':1,
    'parameters_data':json.dumps([{"rank": 0,
    "name_of_field": "length"}])}
MotifType.objects.create(**data)

data = {'name':'rectangle',
    'nb_parameters':2,
    'parameters_data':json.dumps([{"rank": 0,"name_of_field": "length"},{"rank": 1,"name_of_field": "width"}])}
MotifType.objects.create(**data)


# creating some Motif
m=MotifType.objects.get(name='rectangle')

Motif.objects.create(name='rectangle_100_10',type=m,value0=100,value1=10)
Motif.objects.create(name='rectangle_10_5',type=m,value0=10,value1=5)


comment="""
# creating some masks
m=Mask(name='masque1')
m.save()
m.motifs.add(M1)

m=Mask(name='masque2')
m.save()
m.motifs.add(M2)

m=Mask(name='masque12')
m.save()
m.motifs.add(M1)
m.motifs.add(M2)


# querying  motif
# beware expression look the same but one use the Q method to make a and
print(Mask.objects.filter(motifs__type__name='rectangle').filter(Q(motifs__datas__rank='1'),Q(motifs__datas__numeric_value=10)).distinct())

print(Mask.objects.filter(motifs__type__name='rectangle').filter(motifs__datas__rank='1').filter(motifs__datas__numeric_value=10))
"""
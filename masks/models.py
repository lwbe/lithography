from django.db import models


from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField
#from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse





# Create your models here.


class About(models.Model):
    """
    a richtxtfield that can only be editable from the admin page to give a help page.
    """
    content = RichTextField(_("about"))

    def __str__(self):
        return "The content of the about page"


class Usage(models.Model):
    """
    Usage of the mask TLM, TBH,...
    """
    name       = models.CharField(_("Usage"),max_length=100)
    comment    = models.CharField(_("Comment"),max_length=1000)

    # needed for CBV
    def __str__(self):
        return self.name

    @classmethod
    def get_available_fields(cls):
        return ['id','name','comment']

class Localisation(models.Model ):
    """
    Localisation a string to locate where is the mask 
    """
    localisation = models.CharField(_("Localisation"),max_length=100)
    
    def __str__(self) :
        return self.localisation

    @classmethod
    def get_available_fields(cls):
        return ['id','localisation']



class Manufacturer(models.Model):
    """
    Manufacturer : the company that made the mask
    """
    corporateName  = models.CharField(_("Corporate Name"), max_length=100)
    address1       =  models.CharField(_("Address"), max_length=100, default='', blank=True, null=True)
    address2       = models.CharField(_("Address cpl."), max_length=100, default='', blank=True, null=True)
    postcode       = models.CharField(_("Postal Code"), max_length=100, default='', blank=True, null=True)
    city           = models.CharField(_("City"), max_length=100, default='', blank=True, null=True)
    country        = models.CharField(_("Country"), max_length=100, default='', blank=True, null=True)
    email          = models.EmailField(_("@mail"), max_length=100, default='', blank=True, null=True)
    
    def __str__(self):
        return self.corporateName

    @classmethod
    def get_available_fields(cls):
        return ['id',
                'corporateName',
                'address1',
                'address2',
                'postcode',
                'city',
                'country',
                'email']


class MotifType(models.Model):
    name = models.CharField(unique=True,
                            max_length=255,
                            verbose_name="name of the type of motif",
                            help_text="something has to be written here"
                            )

    MAX_PARAM_NB = 10
    PARAM_NB=([(i,str(i)) for i in range(1,MAX_PARAM_NB)])
    nb_parameters = models.IntegerField(verbose_name="the number of parameters",choices=PARAM_NB,default=1)
    #parameters_name=ArrayField(models.CharField(max_length=255))

    # very basic way to handle a certain number of fields better use FK but the form can be simple using some javascript.
    param_name_0 = models.CharField(_("First parameter name"), max_length=255)
    param_name_1 = models.CharField(_("Second parameter name"), max_length=255, default='', blank=True, null=True)
    param_name_2 = models.CharField(_("Third parameter name"), max_length=255, default='', blank=True, null=True)
    param_name_3 = models.CharField(_("Fourth parameter name"), max_length=255, default='', blank=True, null=True)
    param_name_4 = models.CharField(_("Fifth parameter name"), max_length=255, default='', blank=True, null=True)
    param_name_5 = models.CharField(_("Sixth parameter name"), max_length=255, default='', blank=True, null=True)
    param_name_6 = models.CharField(_("Seventh parameter name"), max_length=255, default='', blank=True, null=True)
    param_name_7 = models.CharField(_("Eighth parameter name"), max_length=255, default='', blank=True, null=True)
    param_name_8 = models.CharField(_("Ninth parameter name"), max_length=255, default='', blank=True, null=True)
    param_name_9 = models.CharField(_("Tenth parameter name"), max_length=255, default='', blank=True, null=True)

    comment = models.CharField(_("Comment"),max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_available_fields(cls):
        return ['id',
                'name',
                'nb_parameters',
                'param_name_0',
                'comment']


class Motif(models.Model):
    name = models.CharField(unique=True,
                            max_length=255)
    type = models.ForeignKey(MotifType,on_delete=models.CASCADE)
    step = models.FloatField(_("Step"))
    #values = ArrayField(models.FloatField(blank=True))

    value_0 = models.FloatField(_("First parameter"))
    value_1 = models.FloatField(_("Second parameter"), blank=True, null=True)
    value_2 = models.FloatField(_("Third parameter"), blank=True, null=True)
    value_3 = models.FloatField(_("Fourth parameter"), blank=True, null=True)
    value_4 = models.FloatField(_("Fifth parameter"), blank=True, null=True)
    value_5 = models.FloatField(_("Sixth parameter"), blank=True, null=True)
    value_6 = models.FloatField(_("Seventh parameter"), blank=True, null=True)
    value_7 = models.FloatField(_("Eight parameter"), blank=True, null=True)
    value_8 = models.FloatField(_("Ninth parameter"), blank=True, null=True)
    value_9 = models.FloatField(_("Tenth parameter"),  blank=True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_available_fields(cls):
        return ['id',
                'name',
                'type',
                'step',
                'value_0']

class Mask(models.Model):
    name = models.CharField(unique=True, max_length=255)
    motifs = models.ManyToManyField(Motif)

    polarisationChoices = (('---', 'Select'), ('Positif', 'Positif'), ('Negatif', 'Negatif'))

    idNumber = models.CharField(_("id. number"), max_length=50, default='', unique=True)
    usage = models.ForeignKey(Usage, on_delete=models.PROTECT, blank=True, null=True)
    localisation = models.ForeignKey(Localisation, on_delete=models.PROTECT, blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, blank=True, null=True)
    conceptor = models.CharField(_("Conceptor"), max_length=100, default='', blank=True, null=True)
    level = models.IntegerField(_("Level"), default=1)
    creationYear = models.CharField(_("year of creation"), max_length=10, default='2000')
    GDSFile = models.FileField(_("GDS File"), default='', blank=True, null=True, upload_to="GDS/")
    active = models.BooleanField(_("Active"), default=True)
    polarisation = models.CharField(_("Polarisation"), max_length=20, choices=polarisationChoices, default='Select')
    description = models.TextField("Description", default='', blank=True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_available_fields(cls):
        return ['id',
                'name',
                'motifs',
                'idNumber',
                'usage__name',
                'localisation__localisation',
                'manufacturer__corporateName',
                'conceptor',
                'level',
                'creationYear',
                'GDSFile',
                'active',
                'polarisation',
                'description']


class Image(models.Model):
    image = models.ImageField(upload_to="images/mask")
    mask = models.ForeignKey(Mask,on_delete=models.CASCADE)

    def __str__(self):
        return "img:"+self.mask.name


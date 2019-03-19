from django.db import models


from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse





# Create your models here.


class About(models.Model):
    """
    a richtxtfield tha can only be editable from the admin page to give a help page. 
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


class Localisation(models.Model ):
    """
    Localisation a string to locate where is the mask 
    """
    localisation = models.CharField(_("Localisation"),max_length=100)
    
    def __str__(self) :
        return self.localisation

class Manufacturer(models.Model):
    """
    Manufacturer : the company that made the mask
    """
    corporateName  = models.CharField(_("Corporate Name"), max_length=100)
    address1       =  models.CharField(_("Address"), max_length=100, default='', blank=True, null=True)
    address2       = models.CharField(_("Address"), max_length=100, default='', blank=True, null=True)
    postcode       = models.CharField(_("Postal Code"), max_length=100, default='', blank=True, null=True)
    city           = models.CharField(_("City"), max_length=100, default='', blank=True, null=True)
    country        = models.CharField(_("Country"), max_length=100, default='', blank=True, null=True)
    email          = models.EmailField(_("@mail"), max_length=100, default='', blank=True, null=True)
    
    def __str__(self):
        return self.corporateName  


class MotifType(models.Model):
    name = models.CharField(unique=True,
                            max_length=255,
                            verbose_name="name of the type of motif",
                            help_text="something has to be written here"
                            )
    nb_parameters = models.IntegerField(verbose_name="the number of parameters")
    parameters_data=models.CharField(max_length=2000)
    comment    = models.CharField(_("Comment"),max_length=1000)

    def __str__(self):
        return self.name


class Motif(models.Model):
    name = models.CharField(unique=True,
                            max_length=255)
    type = models.ForeignKey(MotifType,on_delete=models.CASCADE)

    step = models.FloatField(_("Step"))

    # we should set default value to something null?
    value0 = models.FloatField()
    value1 = models.FloatField(blank=True,null=True,default=None)
    value2 = models.FloatField(blank=True,null=True,default=None)
    value3 = models.FloatField(blank=True,null=True,default=None)
    value4 = models.FloatField(blank=True,null=True,default=None)
    value5 = models.FloatField(blank=True,null=True,default=None)
    value6 = models.FloatField(blank=True,null=True,default=None)
    value7 = models.FloatField(blank=True,null=True,default=None)
    value8 = models.FloatField(blank=True,null=True,default=None)
    value9 = models.FloatField(blank=True,null=True,default=None)

    def __str__(self):
        return self.name


class Mask(models.Model):
    name = models.CharField(unique=True, max_length=255)
    motifs=models.ManyToManyField(Motif)

    polarisationChoices = (('---', 'Select'), ('Positif', 'Positif'), ('Negatif', 'Negatif'))

    
    idNumber     = models.CharField(_("id. number"),max_length=50,default='',unique=True)
    usage        = models.ForeignKey(Usage,on_delete=models.PROTECT,blank=True,null=True)
    localisation = models.ForeignKey(Localisation,on_delete=models.PROTECT,blank=True,null=True)
    manufacturer = models.ForeignKey(Manufacturer,on_delete=models.PROTECT,blank=True,null=True)
    conceptor    = models.CharField(_("Conceptor"),max_length=100,default='',blank=True,null=True)
    level        = models.IntegerField(_("Level"),default=1)
    creationYear = models.CharField(_("year of creation"),max_length=10,default='2000')
    GDSFile      = models.FileField(_("GDS File"),default='',blank=True,null=True,upload_to="GDS/")
    active       = models.BooleanField(_("Active"),default=True)
    polarisation = models.CharField(_("Polarisation"),max_length=20,choices=polarisationChoices,default='Select')
    description  = models.TextField("Description",default='',blank=True,null=True)



    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to="images/mask")
    mask = models.ForeignKey(Mask,on_delete=models.CASCADE)

    def __str__(self):
        return "img:"+self.mask.name


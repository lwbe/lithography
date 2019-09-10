from django.db import models
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError


# validator for the idnumber field which is a formatted (?) charfield made of int.
def validate_int(value):
    try:
        int(value)
    except (TypeError, ValueError):
        raise ValidationError(
            _('%(value)s is not an integer'),
            params={'value': value},
        )

# automate the creation of information about the model
def create_cbv_info(d):
    cbv_info = d
    if not cbv_info.get('has_m2m'):
        cbv_info['has_m2m']=False

    # create an index and field_names entry in the dict
    db_fields = [i[0] for i in d['field_info']]
    fields_name = [i[1] for i in d['field_info']]
    index_list = []
    curr_index = 0
    fnames_book = {}
    fnames = []
    for name in fields_name:
        if name in fnames_book:
            index_list.append(fnames_book[name])
        else:
            index_list.append(curr_index)
            fnames_book[name] = curr_index
            curr_index += 1
            fnames.append(name)
    if curr_index == len(fields_name):
        index_list = None
    cbv_info['field_indexes'] = index_list
    cbv_info['field_names'] = fnames
    cbv_info['db_fields'] = db_fields

    return cbv_info


# Create your models here.
class About(models.Model):
    """
    a richtextfield that can only be editable from the admin page to give a help page.
    """
    content = RichTextField(_("about"))

    def __str__(self):
        return "The content of the about page"


class Usage(models.Model):
    """
    Usage of the mask TLM, TBH,...
    """
    name = models.CharField(_("Usage"), max_length=100)
    comment = models.CharField(_("Comment"), max_length=1000)

    # needed for CBV
    cbv_model_info = create_cbv_info(
        {
        'title': 'Utilisations',
        'field_info':
            [
                ('id', 'id'),
                ('name', 'Nom'),
                ('comment', 'Commentaire')
            ]
        }
    )

    def __str__(self):
        return self.name


#--
class Localisation(models.Model ):
    """
    Localisation a string to locate where is the mask 
    """
    localisation = models.CharField(_("Localisation"), max_length=100)

    # needed for CBV
    cbv_model_info = create_cbv_info(
        {'title': 'Localisations',
        'field_info':
            [
                ('id','id'),
                ('localisation','Localisation')
            ]
        }
    )

    def __str__(self):
        return self.localisation

# --
class Manufacturer(models.Model):
    """
    Manufacturer : the company that made the mask
    """
    corporateName = models.CharField(_("Corporate Name"), max_length=100)
    address1 = models.CharField(_("Address"), max_length=100, default='', blank=True, null=True)
    address2 = models.CharField(_("Address cpl."), max_length=100, default='', blank=True, null=True)
    postcode = models.CharField(_("Postal Code"), max_length=100, default='', blank=True, null=True)
    city = models.CharField(_("City"), max_length=100, default='', blank=True, null=True)
    country = models.CharField(_("Country"), max_length=100, default='', blank=True, null=True)
    email = models.EmailField(_("@mail"), max_length=100, default='', blank=True, null=True)

    # needed for CBV
    cbv_model_info = create_cbv_info(
        {'title': 'Fabricants',
        'field_info':
            [
                ('id','id'),
                ('corporateName','Nom'),
                ('address1','Adresse'),
                ('address2','Adresse'),
                ('postcode','Code Postal'),
                ('city','Ville'),
                ('country','Pays'),
                ('email','Courriel')
                ]
        }
    )

    def __str__(self):
        return self.corporateName


# --
class MotifType(models.Model):
    name = models.CharField(unique=True,
                            max_length=255,
                            verbose_name="name of the type of motif",
                            help_text="something has to be written here"
                            )

    MAX_PARAM_NB = 10
    PARAM_NB = ([(i, str(i)) for i in range(1, MAX_PARAM_NB)])
    nb_parameters = models.IntegerField(verbose_name="the number of parameters",
                                        choices=PARAM_NB,
                                        default=1)

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

    def get_params(self):
        return ", ".join([j for i,j in vars(self).items() if (i.startswith('param_name') and j)])

    def __str__(self):
        return self.name

    # needed for CBV
    cbv_model_info = create_cbv_info(
        {'title': 'Type de motifs',
        'field_info': [
            ('id', 'id'),
            ('name', 'Nom'),
            ('nb_parameters','Nb de paramètres'),
            ('param_name_0', 'Paramètre(s)'),
            ('param_name_1', 'Paramètre(s)'),
            ('param_name_2', 'Paramètre(s)'),
            ('param_name_3', 'Paramètre(s)'),
            ('param_name_4', 'Paramètre(s)'),
            ('param_name_5', 'Paramètre(s)'),
            ('param_name_6', 'Paramètre(s)'),
            ('param_name_7', 'Paramètre(s)'),
            ('param_name_8', 'Paramètre(s)'),
            ('param_name_9', 'Paramètre(s)'),
            ('comment', 'Commentaire')
            ]
        }
    )


# --
class Motif(models.Model):
    name = models.CharField(unique=True,
                            max_length=255)
    type = models.ForeignKey(MotifType,on_delete=models.CASCADE)
    step = models.FloatField(_("Step"))
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

    # needed for CBV
    cbv_model_info = create_cbv_info(
        {'title': 'Motifs',
        'field_info':[
            ('id','id'),
            ('name','Nom'),
            ('type','Type'),
            ('step','Pas'),
            ('value_0', 'Valeur'),
            ('value_1', 'Valeur'),
            ('value_2', 'Valeur'),
            ('value_3', 'Valeur'),
            ('value_4', 'Valeur'),
            ('value_5', 'Valeur'),
            ('value_6', 'Valeur'),
            ('value_7', 'Valeur'),
            ('value_8', 'Valeur'),
            ('value_9', 'Valeur'),
            ]
        }
    )

    def get_values(self):
        return ", ".join([j for i,j in vars(self).items() if (i.startswith('value') and j)])

    def __str__(self):
        return self.name

def default_id_number():
    ids = sorted([int(i) for i in list(Mask.objects.all().values_list('idNumber',flat=True))])
    p = ids[0]
    for i in ids[1:]:
        if (i - p) > 1:
            return "%04d" % (p+1)
        p = i
    return "%04d" % (i+1)


# --
class Mask(models.Model):
    polarisationChoices = (
        ('---', 'Select'),
        ('Positif', 'Positif'),
        ('Negatif', 'Negatif')
    )
    conditionChoices = (
        (_('new'), _('new')),
        (_('good'), _('good')),
        (_('bad'), _('bad')),
        (_('broken'), _('broken')),
    )

    name = models.CharField(unique=True, max_length=255)
    motifs = models.ManyToManyField(Motif)

    idNumber = models.CharField(_("id. number"),validators=[validate_int],max_length=50, unique=True,default=default_id_number)
    usage = models.ForeignKey(Usage, on_delete=models.PROTECT, blank=True, null=True)
    localisation = models.ForeignKey(Localisation, on_delete=models.PROTECT, blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, blank=True, null=True)
    conceptor = models.CharField(_("Conceptor"), max_length=100, default='', blank=True, null=True)
    level = models.IntegerField(_("Level"), default=1)
    creationYear = models.CharField(_("year of creation"), max_length=10, default='2000')
    GDSFile = models.FileField(_("GDS File"), default='', blank=True, null=True, upload_to="GDS/")
    #active = models.BooleanField(_("Active"), default=True)
    polarisation = models.CharField(_("Polarisation"), max_length=20, choices=polarisationChoices, default='Select')
    condition = models.CharField(_("Condition"), max_length=7, choices=conditionChoices, default='new')
    description = models.TextField(_("Description"), default='', blank=True, null=True)
    area = models.FloatField(_("Area"), default= 0.0,blank=True, null=True)

    # needed for CBV
    cbv_model_info = create_cbv_info(
        {'title': 'Masques',
        'field_info': [
            ('id', 'id'),
            ('idNumber', 'Identifiant'),
            ('name', 'Nom'),
            ('motifs__name', 'Motif'),
            ('usage__name', 'Utilisation'),
            ('localisation__localisation', 'Localisation'),
            ('manufacturer__corporateName', 'Fabricant'),
            ('conceptor', 'Créateur'),
            ('level', 'Niveau'),
            ('creationYear', 'Année de création'),
            ('GDSFile', 'Fichier GDS'),
            ('condition', 'Etats'),
            ('polarisation', 'Polarisation'),
            ('area', 'Aire'),
            ('description', 'Description')],
         'has_m2m':True
         }
    )

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to="images/mask")
    mask = models.ForeignKey(Mask,on_delete=models.CASCADE)

    def __str__(self):
        return "img:"+self.mask.name


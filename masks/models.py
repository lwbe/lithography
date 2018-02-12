from django.db import models

from django.utils.translation import ugettext_lazy as _
# Create your models here.

class Mask(models.Model):
    name   = models.CharField(_("Nom"),max_length=100,default='')
    number = models.IntegerField(_("Numero"),default=1)


    def __str__(self):
        return self.number

comment = """
class Masques(models.Model):
    choix_polarite=(('---','Select'),('Positif','Positif'),('Negatif','Negatif'))
    #choix_local = (('---','Select'),('Armoiré 1','Armoire1'),('Armoire 2','Armoire2'))
    num = models.CharField("Numero",max_length=50,default='')
    nom = models.CharField("Nom",max_length=100,default='')    
    usage = models.ForeignKey(Usages)
    fabricant=models.ForeignKey(Fabricants,blank=True,null=True)
    concepteur = models.CharField("Concepteur",max_length=100,default='',blank=True,null=True)
    niveau = models.IntegerField("Niveau",default=1)
    local = models.ForeignKey(Localisations)
    description = models.TextField("Description",default='',blank=True,null=True)
    polarite=models.CharField("Polarite",max_length=20,choices=choix_polarite,default='Select')
    
    #datecre = models.DateField("Date de creation (jj/mm/aaaa)",default='2000-01-01',blank=True,null=True)
    
    
    anneecre = models.CharField("Annee de création",max_length=10,default='2000')
    fichierGDS=models.FileField("Fichier GDS",default='',blank=True,null=True,upload_to="GDS/")
    actif=models.BooleanField("Actif",default=True)
    motif = models.ManyToManyField(Motifs)
    
    def __unicode__(self):
        return self.nom  
"""



class Image(models.Model):
    mask = models.ForeignKey(Mask)
    image  = models.ImageField(_("Image"),default='',blank=True,null=True,upload_to="images/")
         
    def __unicode__(self):
         return self.mask.number

    def __str__(self):
        return self.mask.number

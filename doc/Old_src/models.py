# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm
from django.utils import timezone

# Create your models here.

class Usages(models.Model):
    nom = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.nom   
    
class MotifsTypes(models.Model):
    nom = models.CharField(max_length=100)
    nb_dim=models.IntegerField("Nbre dimensions")
    description=models.TextField("Description")
    
    def __unicode__(self):
        return self.nom 

class Localisations(models.Model ):
    nom = models.CharField("Local",max_length=100)
    
    def __unicode__(self) :
        return self.nom 

class Motifs(models.Model) :
    typemotif=models.ForeignKey(MotifsTypes)
    dim1=models.FloatField("Dim 1",default=0,)
    dim2=models.FloatField("Dim 2",default=0,blank=True,null=True)
    dim3=models.FloatField("Dim 3",default=0,blank=True,null=True)
    dim4=models.FloatField("Dim 4",default=0,blank=True,null=True)   
    pas=models.IntegerField("Pas",default=0)
    
    class Meta :
        ordering= ['typemotif__nom','dim1','dim2','dim3','dim4']
        
    def __unicode__(self) :
        
        string = self.typemotif.nom + " / "
        if self.dim1 != 0:
            string+=str(self.dim1) + " / "
        if self.dim2 != 0:
            string+=str(self.dim2) + " / "  
        if self.dim3 != 0:
            string+=str(self.dim3) + " / "   
        if self.dim4 != 0:
            string+=str(self.dim4) + "/" 
        if self.pas == 0 :
            self.pas=" - "
        string+=" - Pas : " + str(self.pas)
        #string= self.typemotif.nom + "/" + str(self.dim1)+ ":" + str(self.dim2)+ ":" + str(self.dim3)+ ":" + str(self.dim4) + " /Pas :"+str(self.pas)
        return string
        
class Fabricants(models.Model):
    rais_soc = models.CharField("Raison sociale",max_length=100)
    add1 = models.CharField("Adresse",max_length=100,default='',blank=True,null=True)
    add2 = models.CharField("Cplt adresse",max_length=100,default='',blank=True,null=True)
    CP = models.CharField("CP",max_length=100,default='',blank=True,null=True)
    ville = models.CharField("Ville",max_length=100,default='',blank=True,null=True)
    pays = models.CharField("Pays",max_length=100,default='',blank=True,null=True)
    email = models.EmailField("@mail",max_length=100,default='',blank=True,null=True)
    
    def __unicode__(self):
        return self.rais_soc  
	
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

class Image(models.Model):
    masque = models.ForeignKey(Masques)
    image  = models.ImageField("Image(s)",default='',blank=True,null=True,upload_to="images/")
 
    def __unicode__(self):
        return self.masque.num
#-------------------------------


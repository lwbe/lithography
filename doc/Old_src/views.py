# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django import forms
from django.forms import ModelForm
from django.forms import formset_factory
from django.db.models import Q
from django.core.files import File
from .models import Usages
from .models import Motifs
from .models import MotifsTypes
from .models import Fabricants
from .models import Masques
from .models import Localisations
from .models import Image
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

def deconnexion(request) :
    message="déconnexion"
    logout(request)
    return HttpResponseRedirect(reverse('masques:home'))


def connexion(request) :
    message = "Vous n'êtes pas connecté" 
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    user = authenticate(username=username, password=password)
    # si utilisateur identifie
    if user is not None :
	message="Connexion OK !"
	login(request, user)
	return HttpResponseRedirect(reverse('masques:masques'))
    #si l'utilisateur n est pas identifie
    else :
	message = "Vous n'êtes pas connecté"
	logout(request)
   
    return render(request,'masques/connexion.html', {'message' : message })
	
##############################################################################   
def traiter_chaine(ch):
    #Traitement des chaines saisies - appel fonction traiter_chaine(ch): 
    # si "50", la fonction retourne [50,50]
    # si "50:40", la fonction retourne [40,50]
    # si ":50", la fonction retourne [-1,50]
    # si "50:", la fonction retourne [50,-1]	    
    separateur=':'
    ch=ch.split(separateur)
    if len(ch)==1:
        ch.append(ch[0])
    if ch[0]=='':
        a=-1
    else:
	try:
	    a=float(ch[0])
	except ValueError:
	    return False
    if ch[1]=='':
        b=-1
    else:
	try:
	    b=float(ch[1])
	except ValueError:
	    return False    
    
    return ([a,b])


################################## FORMULAIRES #############################
################ GENERIC FORM ##########################################
def genericForm(request,id,keys,currentClass,currentForm,returnURL,template,m2m=None,chaine="id"): 
    #si le formulaire est poste
    if request.method == "POST":
	query=None
	# si mode modifier (id=0 pour le mode creation), on ramene les donnees de la table pour pk=id dans le formulaire
	if id!=0:
	    query=currentClass.objects.get(pk=id)
	    
        form = currentForm(request.POST, request.FILES, instance=query)
	#si les saisies sont valides on les sauvegarde
        if form.is_valid():
            form.save()          
        return HttpResponseRedirect(reverse(returnURL))
    # gestion de l'affichage formulaire
    else:
	# si mode creation, alors on affiche un formulaire vide
	if id==0:
	    form=currentForm()
	else:
	    #m2m - il y a des donnees type ManyToMany
	    if m2m:
		m2m_initialdata = dict()
		# pour tous les clefs du tableau 
		for m in m2m:
		    #m est le champ m2m dans la classe (ex motif
		    #on enleve chaque element de clef m de la liste m2m 
		    keys.remove(m) 
		    #Comme la clef m de m2m genere un produit cartesien entre les deux tables m2m, on doit utiliser filter et non get
		    #la methode Django values_liste de m renvoie un tuple dont la premiere valeur est l'id dans la table du m2m (motifs)
		    #m2m
		    
		    
		    m2m_initialdata[m]=[i[0] for i in currentClass.objects.values_list(m).filter(pk=id)]
		#Initialisation des champs de saisie pour tous les attribut qui ne sont pas m2m    
		initialdata = currentClass.objects.values(*keys).get(pk=id)
		#on rajoute ici les valeurs m2m
		#la methode Python update() permet de fusionner deux dictionnaires qui sont ici initialdata et m2m_initialdata
		#le resultat de la fusion est le dictionnaire initialdata
		initialdata.update(m2m_initialdata)
		form=currentForm(initial=initialdata)
	    #il n'y a de donnees type ManyToMany
	    else:	    
		initialdata = currentClass.objects.values(*keys).get(pk=id)
		form=currentForm(initial=initialdata)
	
    return render(request, template , {'form': form})
########################################################################

#[i[0] for i in currentClass.objects.values_list(m).filter(pk=id)]

#l=list()
#for element_tableau in currentClass.objects.values_list(m).filter(pk=id):
#    l.append(element_tableau[0])
###### form Home ###########################################################

#Connexion ##################################################################    


class ConnexionForm(forms.Form):
    username = forms.FloatField() 
    password = forms.FloatField() 
	
###### FABRICANTS ###################################################
def fabricants(request):
    data = Fabricants.objects.order_by('rais_soc')
    return render(request, 'masques/fabricants.html', {'data' : data})

class FabricantForm(forms.ModelForm):
    class Meta:
        model = Fabricants
	fields = "__all__"	
 
@login_required   
def createupdatefabricant(request,id=0):
    keys=['rais_soc','add1','add2','CP','ville','pays','email']
    currentClass = Fabricants
    currentForm = FabricantForm
    returnURL='masques:fabricants'
    template = 'masques/createupdatefabricant.html'
    return genericForm(request,id,keys,currentClass,currentForm,returnURL,template)

###### USAGES ########################################################
def usages(request):
    data = Usages.objects.order_by('nom')
    return render(request, 'masques/usages.html', {'data' : data})

class UsageForm(forms.ModelForm):
    class Meta:
        model = Usages
	fields = "__all__"	

@login_required   
def createupdateusage(request,id=0):
    keys=['nom']
    currentClass = Usages
    currentForm = UsageForm
    returnURL='masques:usages'
    template = 'masques/createupdateusage.html'
    return genericForm(request,id,keys,currentClass,currentForm,returnURL,template)

###### TYPES MOTIFS ################################################
def typemotif(request):
    data = MotifsTypes.objects.all()
    return render(request, 'masques/typemotif.html', {'data' : data})

def detailstypemotif(request,id=0):
    data = MotifsTypes.objects.get(id=id)
    return render(request,'masques/detailstypemotif.html', {'data' : data})

class TypeMotifForm(forms.ModelForm):
    class Meta:
        model = MotifsTypes
	fields = "__all__"

class ListeTypeMotifsForm(forms.Form):
    type_motif = forms.ChoiceField(widget=forms.Select(attrs={'onchange': 'this.form.submit();'})) 

@login_required       
def createupdatetypemotif(request,id=0):
    keys=['nom','nb_dim','description']
    currentClass = MotifsTypes
    currentForm = TypeMotifForm
    returnURL='masques:typemotif'
    template = 'masques/createupdatetypemotif.html'
    return genericForm(request,id,keys,currentClass,currentForm,returnURL,template)



###### MOTIFS #####################################################
def motifs(request):
    message = "Liste des motifs"    
    data = Motifs.objects.order_by('typemotif','dim1','dim2','dim3','dim4','pas')
    return render(request, 'masques/motifs.html', {'data' : data, 'message' : message})

class MotifForm(forms.ModelForm):
    class Meta:
        model = Motifs
	fields = "__all__"

class MotifForm4(forms.Form):
    dim1 = forms.FloatField() 
    dim2 = forms.FloatField() 
    dim3 = forms.FloatField() 
    dim4 = forms.FloatField() 
    pas = forms.IntegerField(required=False,initial=0)
    
class MotifForm3(forms.Form):
    dim1 = forms.FloatField() 
    dim2 = forms.FloatField() 
    dim3 = forms.FloatField() 
    pas = forms.IntegerField(required=False,initial=0)

class MotifForm2(forms.Form):
    dim1 = forms.FloatField() 
    dim2 = forms.FloatField() 
    pas = forms.IntegerField(required=False,initial=0)

class MotifForm1(forms.Form):
    dim1 = forms.FloatField() 
    pas = forms.IntegerField(required=False,initial=0)

def updatemotif(request,id=0):
    message1 = message2 = ""
    doublon = classe = bool = dim1 = dim2 = dim3 = dim4 = nb_dim = 0    
      
    query = Motifs.objects.get(pk=id)
    nb_dim = query.typemotif.nb_dim
    typemotif=query.typemotif
    description=query.typemotif.description      

    if request.method == "POST":
	
	if nb_dim == 1:
	    form = MotifForm1(request.POST)
	elif nb_dim == 2:
	    form = MotifForm2(request.POST)	
	elif nb_dim == 3:
	    form = MotifForm3(request.POST)
	elif nb_dim == 4:
	    form = MotifForm4(request.POST)		
        if form.is_valid():
	    pas = form.cleaned_data['pas']
	    if nb_dim == 1 :
		dim1 = form.cleaned_data['dim1']
	    if nb_dim == 2 :
		dim1 = form.cleaned_data['dim1']
		dim2 = form.cleaned_data['dim2']
	    if nb_dim == 3 :
		dim1 = form.cleaned_data['dim1']
		dim2 = form.cleaned_data['dim2']
		dim3 = form.cleaned_data['dim3']	    
	    if nb_dim == 4 :
		dim1 = form.cleaned_data['dim1']
		dim2 = form.cleaned_data['dim2']
		dim3 = form.cleaned_data['dim3']	
		dim4 = form.cleaned_data['dim4']
	    
	    query.dim1 = dim1
	    query.dim2 = dim2
	    query.dim3 = dim3
	    query.dim4 = dim4
	    query.pas = pas
	    
	    #Test de classement des saisies sur dimension
	    if nb_dim == 4 :
		if dim1 <= dim2 <= dim3 <= dim4 :
		    classe = 1
	    if nb_dim == 3 :
		if dim1 <= dim2 <= dim3 :
		    classe = 1
	    if nb_dim == 2 :
		if dim1 <= dim2 :
		    classe = 1
	    if nb_dim == 1 :
		classe = 1
	    
	    #Traitement des doublons
	    query2 = Motifs.objects.filter(dim1 = dim1, dim2 = dim2, dim3 = dim3, dim4 = dim4, pas = pas)
	    mot=[]
	    mot = [m.id for m in query2]
	   
	    #Le id passe en parametre est une chaine de caracteres ! il faut le transformer en integer
	    if int(id) in mot :
		mot.remove(int(id))
	    
	    if len(mot) > 0 :
		doublon = 1
		message1 = "Ce motif existe dans la BDD !"
	    
	    if classe == 0 :
		message2="Les dimensions ne sont pas saisies par ordre croissant"	
		
    
	    #Les dimensions sont classees et il ne s'agit pas de doublon
	    if classe == 1 and doublon == 0 :
		query.save()
		return HttpResponseRedirect(reverse('masques:motifs'))
		
    else:
	data = Motifs.objects.values('typemotif','dim1','dim2','dim3','dim4','pas').get(pk=id)
	if nb_dim==1:
	    form=MotifForm1(initial=data)
	elif nb_dim==2:
	    form=MotifForm2(initial=data)	
	elif nb_dim==3:
	    form=MotifForm3(initial=data)
	elif nb_dim==4:
	    form=MotifForm4(initial=data)	    
	
    return render(request, 'masques/updatemotif.html' , {'form':form,'typemotif':typemotif,'description':description,'message1':message1,'message2':message2})


def createmotif(request):
    description = message1 = message2 = ""
    doublon = classe = bool = dim1 = dim2 = dim3 = dim4 = nb_dim = 0
   
    form = ListeTypeMotifsForm()
    form.fields['type_motif'].choices = [("select","select")]+[ (i,i) for i in MotifsTypes.objects.all()]  
    if request.method == "POST":
	form = ListeTypeMotifsForm(request.POST)
	form.fields['type_motif'].choices = [ (i,i) for i in MotifsTypes.objects.all()]
	
	if "type_motif" in request.POST:
	    #Booleen qui permet d'afficher le bouton "enregistrer" des qu'il y a selection sur type motif
	    bool=1
	    if form.is_valid():
		type_motif=form.cleaned_data['type_motif']
		query = MotifsTypes.objects.get(nom=type_motif)
		nb_dim = query.nb_dim
		description = query.description
		if nb_dim == 1 :
		    form2 = MotifForm1()		
		elif nb_dim == 2 :
		    form2 = MotifForm2()			    
		elif nb_dim == 3 :
		    form2 = MotifForm3()
		elif nb_dim == 4:
		    form2 = MotifForm4()
		    
	    #return render(request, 'masques/motifs.html', {'form' : form,'form2' : form2,'nb_dim':nb_dim,'description':description})
	
	if "enregistrer" in request.POST:
	    if form.is_valid():
		type_motif = form.cleaned_data['type_motif']
		query = MotifsTypes.objects.get(nom=type_motif)
		nb_dim = query.nb_dim
		id_type_motif = query.id
		
		if nb_dim == 1 :	    
		    form2 = MotifForm1(request.POST)
		    if form2.is_valid() :
			dim1 = form2.cleaned_data['dim1']
			pas = form2.cleaned_data['pas']
			#les dimensions sont forcement classee car une seule dimension
			classe = 1
		    
		elif nb_dim == 2 :
		    form2 = MotifForm2(request.POST)
		    if form2.is_valid():
			dim1 = form2.cleaned_data['dim1']
			dim2 = form2.cleaned_data['dim2']
			pas = form2.cleaned_data['pas']
			if dim1 <= dim2 :
			    classe = 1			
	
		elif nb_dim == 3 :
		    form2 = MotifForm3(request.POST)
		    if form2.is_valid():
			dim1 = form2.cleaned_data['dim1']
			dim2 = form2.cleaned_data['dim2']
			dim3 = form2.cleaned_data['dim3']
			pas = form2.cleaned_data['pas']
			if dim1 <= dim2 <= dim3 :
			    classe = 1			
		
		elif nb_dim == 4 :
		    form2 = MotifForm4(request.POST)
		    if form2.is_valid():
			dim1 = form2.cleaned_data['dim1']
			dim2 = form2.cleaned_data['dim2']
			dim3 = form2.cleaned_data['dim3']
			dim4 = form2.cleaned_data['dim4']
			pas = form2.cleaned_data['pas']
			if dim1 <= dim2 <= dim3 <= dim4 :
			    classe = 1
		
		
		#Traitement des doublons
		count_motif = Motifs.objects.filter(dim1=dim1,dim2=dim2,dim3=dim3,dim4=dim4,pas=pas).count()
		if count_motif > 0 :
		    doublon = 1
		    message1 = "Ce motif existe dans la BDD !"
		 
		if classe == 0 :
		     message2="Les dimensions ne sont pas saisies dans l'ordre croissant !"
		
		#On enregistre les donnees si les dim sont classees et si il n'y a pas de doublon    
		if classe == 1 and doublon ==  0 :   
		    Motifs.objects.create(typemotif_id = id_type_motif,dim1 = dim1,dim2 = dim2,dim3 = dim3,dim4 = dim4,pas=pas)
		    return HttpResponseRedirect(reverse('masques:motifs'))
		
    else: # cas du GET
	form2 = None 
	
    return render(request, 'masques/createmotif.html', {'form' : form,'form2' : form2,'description':description,'bool':bool,'message1':message1,'message2':message2})


###### LOCALISATIONS #####################################################
def localisations(request):     
    data = Localisations.objects.all()
    return render(request, 'masques/localisations.html', {'data' : data})

class LocalisationForm(forms.ModelForm) :
    class Meta:
        model = Localisations
	fields = "__all__"
	
@login_required   
def createupdatelocalisation(request,id=0) :
    keys=['nom']
    currentClass = Localisations
    currentForm = LocalisationForm
    returnURL='masques:localisations'
    template = 'masques/createupdatelocalisation.html'
    return genericForm(request,id,keys,currentClass,currentForm,returnURL,template)

###### IMAGES #########################################################
def help(request) :
    return render(request, 'masques/help.html', {})

def imagesmasque(request,id=0) :
  
    form=ImageForm()
    if request.method == "POST":
	imid=[k for k,v in request.POST.iteritems() if v== "supprimer"]
	if imid :
	    imageobject=Image.objects.get(id=imid[0])
	    imageobject.delete()
    
	if 'ajouter-image' in request.POST :
	    form=ImageForm(request.POST,request.FILES)
	    if form.is_valid():
		image_chargee=request.FILES['image']
		image=Image.objects.create(masque=Masques.objects.get(pk=id),image=image_chargee)
	   
	
    
    
    data = Masques.objects.get(pk=id)
    return render(request, 'masques/imagesmasque.html', {'data' : data,'form' : form})

def imagesmasque2(request,id=0):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
	    print "valide"
            image = Image.objects.create(Masques=Masques.objects.get(pk=id),image=request.FILES['image'])
            image.save()
	else :
	    print "invalide"
            
    else:
        form = ImageForm()
    
    data = Masques.objects.get(pk=id)
    return render(request,  'masques/imagesmasque.html', {'data' : data,'form': form})

def zoomimage1(request,id=0) :
    data=Image.objects.get(id=id)
    return render(request, 'masques/zoomimage1.html', {'data' : data}) 

def zoomimage2(request,id=0) :
    data=Image.objects.get(id=id)
    return render(request, 'masques/zoomimage2.html', {'data' : data}) 

class ImageForm2(forms.ModelForm) :
    class Meta:
	model = Image
	#fields = "__all__"
	fields=['image']

class ImageForm(forms.Form):
    #image  = forms.ImageField(required="False",upload_to="images/")
    image  = forms.ImageField(required="False",widget=forms.ClearableFileInput(attrs={'multiple': True}))

###### MASQUES ########################################################

def masques(request) :
    data = Masques.objects.order_by('usage','nom')
    message="Liste de tous les masques"
    return render(request, 'masques/masques.html', {'data' : data,'message' : message})

def masquesparmotif(request,id=0) :
    if id != 0:
	query = Motifs.objects.get(pk=id)
	type_motif = query.typemotif
	dim1 = query.dim1
	dim2 = query.dim2
	dim3 = query.dim3
	dim4 = query.dim4
	pas = query.pas
	
	message = "Liste de tous les masques de motif : " + str(type_motif) + " ( " + str(dim1)
	if dim2 != 0:
	    message+= ' / ' + str(dim2)
	if dim3 != 0:
	    message+= ' / ' + str(dim3)	
	if dim4 != 0:
	    message+= ' / ' + str(dim4)	
	message+= ' ) '
	
	message+= ' - Pas : '  + str(pas)
	
	data = Masques.objects.order_by('usage','nom').filter(motif__id=id)
	
    else: 
	data = None
	message="Pas de masques"
    return render(request, 'masques/masques.html', {'data' : data,'message' : message})


def masquesparusage(request,id=0) :
    if id != 0:
	#détails sur usage passé en paramètre (id) pour éditer le message transmis
	query = Usages.objects.get(pk=id)
	nom_usage = query.nom
	message = "Liste de tous les masques / usage : " + nom_usage
	
	data = Masques.objects.order_by('usage','nom').filter(usage__id=id)
	
    else: 
	data = None
	message="Pas de masques"
    return render(request, 'masques/masques.html', {'data' : data,'message' : message})

def masquesparlocal(request,id=0) :
    if id != 0:
	#détails sur usage passé en paramètre (id) pour éditer le message transmis
	query = Localisations.objects.get(pk=id)
	nom_local = query.nom
	message = "Liste de tous les masques / localisation : " + nom_local
	
	data = Masques.objects.order_by('local','nom').filter(local__id=id)
	
    else: 
	data = None
	message="Pas de masques"
    return render(request, 'masques/masques.html', {'data' : data,'message' : message})

def detailsmasque(request,id=0) :
    data = Masques.objects.order_by('typemotif').get(id=id)
    return render(request, 'masques/detailsmasque.html', {'data' : data})

  

class MasqueForm(forms.ModelForm) :
    class Meta:
        model = Masques
	fields = "__all__"
	

@login_required   
def createupdatemasque(request,id=0) :
    keys=['num','nom','local','usage','polarite','niveau','anneecre','fabricant','concepteur','motif','fichierGDS','description','actif']
    currentClass = Masques
    currentForm = MasqueForm
    returnURL='masques:masques'
    template = 'masques/createupdatemasque.html'
    variable_m2m = ['motif']
    #ch='motif__typemotif__nom'
    return genericForm(request,id,keys,currentClass,currentForm,returnURL,template,m2m=variable_m2m)



def searchMasques(request) :
    form = ListeTypeMotifsForm()
    form.fields['type_motif'].choices = [("select","select")]+[(i,i) for i in MotifsTypes.objects.all()]   
    nb_dim = 0
    description = ""
    message = "Resultat de la recherche de masques de motif(s) "
    if request.method == "POST":
	form = ListeTypeMotifsForm(request.POST)
	form.fields['type_motif'].choices = [("select","select")]+[ (i,i) for i in MotifsTypes.objects.all()]  
	
	if "type_motif" in request.POST :
	    if form.is_valid():
		type_motif=form.cleaned_data['type_motif']
		query = MotifsTypes.objects.get(nom=type_motif)
		nb_dim=query.nb_dim
		description=query.description
		if nb_dim == 1:
		    form2 = SearchMasquesForm1()		
		elif nb_dim == 2:
		    form2 = SearchMasquesForm2()			    
		elif nb_dim == 3:
		    form2 = SearchMasquesForm3()
		elif nb_dim == 4:
		    form2 = SearchMasquesForm4()
		    
	    #return render(request, 'masques/home.html', {'form' : form,'form2' : form2,'nb_dim':nb_dim,'description':description,'liste':liste})
	#Traitement des donnees - recherche des masques
	if "recherche" in request.POST:
	    if form.is_valid():
		type_motif=form.cleaned_data['type_motif']
		query = MotifsTypes.objects.get(nom=type_motif)
		nb_dim=query.nb_dim
		
		if nb_dim == 1 :	    
		    form2 = SearchMasquesForm1(request.POST)
		    
		elif nb_dim == 2 :
		    form2 = SearchMasquesForm2(request.POST)
		   
		elif nb_dim == 3 :
		    form2 = SearchMasquesForm3(request.POST)
		
		elif nb_dim == 4 :
		    form2 = SearchMasquesForm4(request.POST)
		    
		if form2.is_valid() :
		    message += type_motif + " ( "
		    #Recuperation des champs du formulaire		
		    listefield=form2.fields.keys()
		    #On enleve le pas de la liste des champs du formulaire
		    listefield.remove('pas')
		    #filtervalue = {'motif__pas'            : form2.cleaned_data['pas'],
		    #             'motif__typemotif__nom' : form.cleaned_data['type_motif']}
		    
		    filtervalue = {'motif__typemotif__nom' : form.cleaned_data['type_motif']}	
		    
		    for f in listefield :
			ch_dim = form2.cleaned_data[f]
			if len(ch_dim) == 0 :
			    ch_dim="00:00"
			#Construction du message utilisateur
			if ch_dim <> "00:00" :
			    message+=" ["+ ch_dim +"]"		    
			ch_dim = ch_dim.replace(",",".")
		   	   
			liste_dim = traiter_chaine(ch_dim)
			#Message d'erreur - si return fonction = false
			if not liste_dim :
			    message = "Mauvaise saisie ! Vous devez saisir les donnees sous le format xx:yy. xx et yy doivent etre numeriques"
			    return render(request, 'masques/home.html', {'form' : form,'form2' : form2,'nb_dim':nb_dim,'description':description,'message':message})			
			if liste_dim[0] >= 0 :
			    filtervalue["motif__"+f.replace('ch_','') + '__gte'] = liste_dim[0]
			if liste_dim[1] >= 0 :
			    filtervalue["motif__"+f.replace('ch_','') + '__lte'] = liste_dim[1]		    
	    
		    #message+=" ) - Pas : "+str(form2.cleaned_data['pas'])
		    message+=" ) "
		
		    data = Masques.objects.filter(**filtervalue).distinct()
		   
		    return render(request,'masques/masques.html', {'data': data,'message':message})
		
    else: # cas du GET
	form2 = None 
	
    return render(request, 'masques/home.html', {'form' : form,'form2' : form2,'nb_dim':nb_dim,'description':description})
    


def searchMasques1(request):
    
    form = ListeTypeMotifsForm()
    form.fields['type_motif'].choices = [("select","select")]+[ (i,i) for i in MotifsTypes.objects.all()]   
    nb_dim=0
    separateur=':'
    ch_dim1=""
    ch_dim2=""
    ch_dim3=""
    ch_dim4=""
    ch_pas=0
    message=""
    description=""
   

    if request.method == "POST":
	form = ListeTypeMotifsForm(request.POST)
	#form.fields['type_motif'].choices = [ (i,i) for i in MotifsTypes.objects.all()]
	form.fields['type_motif'].choices = [("select","select")]+[ (i,i) for i in MotifsTypes.objects.all()]  
	
	if "type_motif" in request.POST:
	    if form.is_valid():
		type_motif=form.cleaned_data['type_motif']
		query = MotifsTypes.objects.get(nom=type_motif)
		nb_dim=query.nb_dim
		description=query.description
		if nb_dim==1:
		    form2 = SearchMasquesForm1()		
		elif nb_dim==2:
		    form2 = SearchMasquesForm2()			    
		elif nb_dim==3:
		    form2 = SearchMasquesForm3()
		elif nb_dim==4:
		    form2 = SearchMasquesForm4()
		    
	    #return render(request, 'masques/home.html', {'form' : form,'form2' : form2,'nb_dim':nb_dim,'description':description,'liste':liste})
	#Traitement des donnees - recherche des masques
	if "recherche" in request.POST:
	    if form.is_valid():
		type_motif=form.cleaned_data['type_motif']
		query = MotifsTypes.objects.get(nom=type_motif)
		nb_dim=query.nb_dim
		
		if nb_dim==1:	    
		    form2 = SearchMasquesForm1(request.POST)

		    if form2.is_valid() :
			ch_dim1=form2.cleaned_data['ch_dim1']
			ch_pas=form2.cleaned_data['pas']
		    
		elif nb_dim==2:
		    form2 = SearchMasquesForm2(request.POST)
		    if form2.is_valid():
			ch_dim1=form2.cleaned_data['ch_dim1']
			ch_dim2=form2.cleaned_data['ch_dim2']
			ch_pas=form2.cleaned_data['pas']
	
		elif nb_dim==3:
		    form2 = SearchMasquesForm3(request.POST)
		    if form2.is_valid():
			ch_dim1=form2.cleaned_data['ch_dim1']
			ch_dim2=form2.cleaned_data['ch_dim2']
			ch_dim3=form2.cleaned_data['ch_dim3']
			ch_pas=form2.cleaned_data['pas']
		
		elif nb_dim==4:
		    form2 = SearchMasquesForm4(request.POST)
		    if form2.is_valid():
			ch_dim1=form2.cleaned_data['ch_dim1']
			ch_dim2=form2.cleaned_data['ch_dim2']
			ch_dim3=form2.cleaned_data['ch_dim3']
			ch_dim4=form2.cleaned_data['ch_dim4']
			ch_pas=form2.cleaned_data['pas']		
	    
		if len(ch_dim4)==0:
		    ch_dim4="00:00"	
		if len(ch_dim3)==0:
		    ch_dim3="00:00"
		if len(ch_dim2)==0:
		    ch_dim2="00:00"
		if len(ch_dim1)==0:
		    ch_dim1="00:00"
		
		ch_dim1 = ch_dim1.replace(",",".")
		ch_dim2 = ch_dim2.replace(",",".")
		ch_dim3 = ch_dim3.replace(",",".")
		ch_dim4 = ch_dim4.replace(",",".")
		
		#Traitement des chaines saisies - appel fonction traiter_chaine(ch): 
		# si "50", la fonction retourne [50,50]
		# si "50:40", la fonction retourne [40,50]
		# si ":50", la fonction retourne [-1,50]
		# si "50:", la fonction retourne [50,-1]
		liste_dim1=traiter_chaine(ch_dim1)
		liste_dim2=traiter_chaine(ch_dim2)
		liste_dim3=traiter_chaine(ch_dim3)
		liste_dim4=traiter_chaine(ch_dim4)	
		
		if not liste_dim1 or not liste_dim2 or not liste_dim3 or not liste_dim4 :
		    message="Mauvaise saisie ! Vous devez saisir les donnees sous le format xx:yy. xx et yy doivent etre numeriques"
		    return render(request, 'masques/home.html', {'form' : form,'form2' : form2,'nb_dim':nb_dim,'description':description,'message':message})
		
		#Edition du message a transmettre dans masques.html - recapitulatif des donnees saisies
		message = "Liste des masques de motif " +  type_motif + " ( "
		if ch_dim1 <> "00:00" :
		    message+=" ["+ ch_dim1+"]"
		if ch_dim2 <> "00:00" :
		    message+=" / ["+ ch_dim2+"]"
		if ch_dim3 <> "00:00" :
		    message+=" / ["+ ch_dim3+"]"	
		if ch_dim4 <> "00:00" :
		    message+=" / ["+ ch_dim4+"]"	
		message+=" ) - Pas : "+str(ch_pas)
		
		#Edition de la requete de recherche de masques qui comportent les motifs correspondants aux criteres de recherche
		#On commence par rechercher les motifs correspondants
		QUERY2 = Motifs.objects.values('masques')
		ruls=Q(typemotif__nom=type_motif,pas=ch_pas)
		#Traitement 1er champ de saisie dim1 - encadrement min max. On ne traite pas les cas -1
		if liste_dim1[0] >= 0:
		    ruls=ruls&Q(dim1__gte=liste_dim1[0])
		if liste_dim1[1] >= 0:
		    ruls=ruls&Q(dim1__lte=liste_dim1[1])
		#Traitement 2eme champ de saisie dim2 - encadrement min max. On ne traite pas les cas -1
		if liste_dim2[0] >= 0:
		    ruls=ruls&Q(dim2__gte=liste_dim2[0])
		if liste_dim2[1] >= 0:
		    ruls=ruls&Q(dim2__lte=liste_dim2[1])
		#Traitement 3eme champ de saisie dim2 - encadrement min max. On ne traite pas les cas -1
		if liste_dim3[0] >= 0:
		    ruls=ruls&Q(dim3__gte=liste_dim3[0])
		if liste_dim3[1] >= 0:
		    ruls=ruls&Q(dim3__lte=liste_dim3[1])
		#Traitement 3eme champ de saisie dim2 - encadrement min max. On ne traite pas les cas -1
		if liste_dim4[0] >= 0:
		    ruls=ruls&Q(dim4__gte=liste_dim4[0])
		if liste_dim4[1] >= 0:
		    ruls=ruls&Q(dim4__lte=liste_dim4[1])		   
		QUERY2 = QUERY2.filter(ruls)
		# On recherche les masques qui correspondent aux motifs trouves
		masques_id=[]
		for m in QUERY2:
		    masques_id.append(m['masques'])      
		data = Masques.objects.filter(id__in=masques_id).distinct()
		       
		return render(request,'masques/masques.html', {'data': data,'message':message}) 	    	    
    else: # cas du GET
	form2 = None 
	
    return render(request, 'masques/home.html', {'form' : form,'form2' : form2,'nb_dim':nb_dim,'description':description})
       
class SearchMasquesForm4(forms.Form):
    #type_motif = forms.ChoiceField() 
    ch_dim1 = forms.CharField(required=False,max_length=15) 
    ch_dim2 = forms.CharField(required=False,max_length=15)
    ch_dim3 = forms.CharField(required=False,max_length=15)
    ch_dim4 = forms.CharField(required=False,max_length=15)
    pas = forms.IntegerField(required=False,initial=0)
    
class SearchMasquesForm3(forms.Form):
    # type_motif = forms.ChoiceField() 
    ch_dim1 = forms.CharField(required=False,max_length=15) 
    ch_dim2 = forms.CharField(required=False,max_length=15)
    ch_dim3 = forms.CharField(required=False,max_length=15)
    pas = forms.IntegerField(required=False,initial=0)
    
	
class SearchMasquesForm2(forms.Form):
    #type_motif = forms.ChoiceField() 
    ch_dim1 = forms.CharField(required=False,max_length=15) 
    ch_dim2 = forms.CharField(required=False,max_length=15)
    pas = forms.IntegerField(required=False,initial=0)
	
	
class SearchMasquesForm1(forms.Form):
    #type_motif = forms.ChoiceField() 
    ch_dim1 = forms.CharField(required=False,max_length=15) 
    pas = forms.IntegerField(required=False,initial=0)


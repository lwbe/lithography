from peewee import *

if len(sys.argv) != 2:
    print("please give the directory where the old data are")


#MEDIA='../../OriginalData/media/'
#PATH_TO_MANAGE_PY="../"
#PATH_TO_ORIGINAL_DB='../../OriginalData/masques.sqlite3'
MEDIA=sys.argv[1]+"/media/"
PATH_TO_MANAGE_PY="../"
PATH_TO_ORIGINAL_DB=sys.argv[1]+"/masques.sqlite3"


database = SqliteDatabase(PATH_TO_ORIGINAL_DB, **{})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class AuthGroup(BaseModel):
    name = CharField(unique=True)

    class Meta:
        table_name = 'auth_group'

class DjangoContentType(BaseModel):
    app_label = CharField()
    model = CharField()

    class Meta:
        table_name = 'django_content_type'
        indexes = (
            (('app_label', 'model'), True),
        )

class AuthPermission(BaseModel):
    codename = CharField()
    content_type = ForeignKeyField(column_name='content_type_id', field='id', model=DjangoContentType)
    name = CharField()

    class Meta:
        table_name = 'auth_permission'
        indexes = (
            (('content_type', 'codename'), True),
        )

class AuthGroupPermissions(BaseModel):
    group = ForeignKeyField(column_name='group_id', field='id', model=AuthGroup)
    permission = ForeignKeyField(column_name='permission_id', field='id', model=AuthPermission)

    class Meta:
        table_name = 'auth_group_permissions'
        indexes = (
            (('group', 'permission'), True),
        )

class AuthUser(BaseModel):
    date_joined = DateTimeField()
    email = CharField()
    first_name = CharField()
    is_active = BooleanField()
    is_staff = BooleanField()
    is_superuser = BooleanField()
    last_login = DateTimeField(null=True)
    last_name = CharField()
    password = CharField()
    username = CharField(unique=True)

    class Meta:
        table_name = 'auth_user'

class AuthUserGroups(BaseModel):
    group = ForeignKeyField(column_name='group_id', field='id', model=AuthGroup)
    user = ForeignKeyField(column_name='user_id', field='id', model=AuthUser)

    class Meta:
        table_name = 'auth_user_groups'
        indexes = (
            (('user', 'group'), True),
        )

class AuthUserUserPermissions(BaseModel):
    permission = ForeignKeyField(column_name='permission_id', field='id', model=AuthPermission)
    user = ForeignKeyField(column_name='user_id', field='id', model=AuthUser)

    class Meta:
        table_name = 'auth_user_user_permissions'
        indexes = (
            (('user', 'permission'), True),
        )

class DjangoAdminLog(BaseModel):
    action_flag = IntegerField()
    action_time = DateTimeField()
    change_message = TextField()
    content_type = ForeignKeyField(column_name='content_type_id', field='id', model=DjangoContentType, null=True)
    object = TextField(column_name='object_id', null=True)
    object_repr = CharField()
    user = ForeignKeyField(column_name='user_id', field='id', model=AuthUser)

    class Meta:
        table_name = 'django_admin_log'

class DjangoMigrations(BaseModel):
    app = CharField()
    applied = DateTimeField()
    name = CharField()

    class Meta:
        table_name = 'django_migrations'

class DjangoSession(BaseModel):
    expire_date = DateTimeField(index=True)
    session_data = TextField()
    session_key = CharField(primary_key=True)

    class Meta:
        table_name = 'django_session'

class MasquesFabricants(BaseModel):
    cp = CharField(column_name='CP', null=True)
    add1 = CharField(null=True)
    add2 = CharField(null=True)
    email = CharField(null=True)
    pays = CharField(null=True)
    rais_soc = CharField()
    ville = CharField(null=True)

    class Meta:
        table_name = 'masques_fabricants'

class MasquesUsages(BaseModel):
    nom = CharField()

    class Meta:
        table_name = 'masques_usages'

class MasquesLocalisations(BaseModel):
    nom = CharField()

    class Meta:
        table_name = 'masques_localisations'

class MasquesMasques(BaseModel):
    actif = BooleanField()
    anneecre = CharField()
    concepteur = CharField(null=True)
    description = TextField(null=True)
    fabricant = ForeignKeyField(column_name='fabricant_id', field='id', model=MasquesFabricants, null=True)
    fichiergds = CharField(column_name='fichierGDS', null=True)
    local = ForeignKeyField(column_name='local_id', field='id', model=MasquesLocalisations)
    niveau = IntegerField()
    nom = CharField()
    num = CharField()
    polarite = CharField()
    usage = ForeignKeyField(column_name='usage_id', field='id', model=MasquesUsages)

    class Meta:
        table_name = 'masques_masques'

class MasquesImage(BaseModel):
    image = CharField(null=True)
    masque = ForeignKeyField(column_name='masque_id', field='id', model=MasquesMasques)

    class Meta:
        table_name = 'masques_image'

class MasquesMotifstypes(BaseModel):
    description = TextField()
    nb_dim = IntegerField()
    nom = CharField()

    class Meta:
        table_name = 'masques_motifstypes'

class MasquesMotifs(BaseModel):
    dim1 = FloatField()
    dim2 = FloatField(null=True)
    dim3 = FloatField(null=True)
    dim4 = FloatField(null=True)
    pas = IntegerField()
    typemotif = ForeignKeyField(column_name='typemotif_id', field='id', model=MasquesMotifstypes)

    class Meta:
        table_name = 'masques_motifs'

class MasquesMasquesMotif(BaseModel):
    masques = ForeignKeyField(column_name='masques_id', field='id', model=MasquesMasques)
    motifs = ForeignKeyField(column_name='motifs_id', field='id', model=MasquesMotifs)

    class Meta:
        table_name = 'masques_masques_motif'

class SqliteSequence(BaseModel):
    name = UnknownField(null=True)  # 
    seq = UnknownField(null=True)  # 

    class Meta:
        table_name = 'sqlite_sequence'
        primary_key = False

if  __name__ == '__main__':

    import json
    import os,django,sys

    from django.db.models import Q
    sys.path.append(PATH_TO_MANAGE_PY)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lithography.settings")
    django.setup()

    from django.contrib.auth.models import User
    if User.objects.filter(username='admin'):
        pass
    else:
        User.objects.create_superuser('admin', 'admin@example.com', '@dm1n')

    from django.core.files import File

    from masks.models import Mask,Motif,MotifType,Manufacturer,Localisation,Usage,Image
    import json

    #remove all the data
    MotifType.objects.all().delete()
    Motif.objects.all().delete()
    Mask.objects.all().delete()
    Manufacturer.objects.all().delete()
    Localisation.objects.all().delete()
    Usage.objects.all().delete()
    Image.objects.all().delete()

    definition = """
    OLD DATABASE             NEW DATABASE

    Usage                      Usage
    nom                         name
                                comment
    """


    for u in MasquesUsages().select():
        Usage.objects.create(name=u.nom)

    print(Usage.objects.all())

    definition = """
OLD DATABASE             NEW DATABASE


Localisation               Localisation
  nom                          localisation

"""

    for l in MasquesLocalisations().select():
        Localisation.objects.create(localisation=l.nom)

    print(Localisation.objects.all())

    definition = """
OLD DATABASE             NEW DATABASE

Fabricants                 Manufacturer(models.Model):
    cp                        postcode
    add1                      address1
    add2                      address2
    email                     email
    pays                      country   
    rais_soc                  corporateName
    ville                     city
"""

    for f in MasquesFabricants().select():
        Manufacturer.objects.create(postcode=f.cp,
        address1=f.add1,
        address2=f.add2,
        email=f.email,
        country=f.pays,
        corporateName=f.rais_soc,
        city=f.ville)

    print(Manufacturer.objects.all())


    definition = """
OLD DATABASE             NEW DATABASE
MasquesMotifstypes         MotifType
    description              comment
    nb_dim                   nb_parameters
    nom                      name
                             parameters_data

    """
    #'[{"rank": 0, "name_of_field": "q"}, {"rank": 1, "name_of_field": "qq"}]'

    for mt in MasquesMotifstypes().select():
        if mt.nb_dim == 1:
            MotifType.objects.create(name=mt.nom, nb_parameters=mt.nb_dim, comment=mt.description, param_name_0='largeur')
        elif mt.nb_dim == 2:
            MotifType.objects.create(name=mt.nom, nb_parameters=mt.nb_dim, comment=mt.description, param_name_0='largeur',param_name_1='longueur')
        elif mt.nb_dim == 3:
            MotifType.objects.create(name=mt.nom, nb_parameters=mt.nb_dim, comment=mt.description, param_name_0='largeur',param_name_1='longueur',param_name_2='autre')
        else:
            print("unknown number of dimension ",mt.nb_dim," pour ",mt.nom)

    old="""                                                                                                   
    for mt in MasquesMotifstypes().select():
        print(mt.nom,mt.nb_dim)
        if mt.nb_dim == 1:
            p = ["largeur"]
        elif mt.nb_dim == 2:
            p = ["largeur","longueur"]

        MotifType.objects.create(name=mt.nom,
                             nb_parameters=mt.nb_dim,
                             comment=mt.description,
                             parameters_name=p)
    """

    definition = """
OLD DATABASE             NEW DATABASE
MasquesMotifs              Motif
    pas                       step
    typemotif                 type
    dim1                      value0
    dim2                      value1
    dim3                      value2
    dim4                      value3
                              name

    """

    ids={}
    for m in MasquesMotifs().select():
        print("%s_%sx%s:%s" % (m.typemotif.nom,m.dim1,m.dim2,m.pas))
        nb_dim = m.typemotif.nb_dim
        if nb_dim == 1:
            name="%s_%s:%s" % (m.typemotif.nom,m.dim1,m.pas)
        elif nb_dim == 2:
            name="%s_%sx%s:%s" % (m.typemotif.nom,m.dim1,m.dim2,m.pas)
        elif nb_dim == 3:
            name="%s_%sx%sx%s:%s" % (m.typemotif.nom,m.dim1,m.dim2,m.dim3,m.pas)
        elif nb_dim == 4:
            name="%s_%sx%sx%sx%s:%s" % (m.typemotif.nom,m.dim1,m.dim2,m.dim3,m.dim4,m.pas)

        print(m.pas)
        n = Motif.objects.create(name=name,
                             step=m.pas,
                             type=MotifType.objects.get(name=m.typemotif.nom),
                             value_0=float(m.dim1),
                             value_1=float(m.dim2) if m.dim2 != 0.0 else None ,
                             value_2=float(m.dim3) if m.dim3 != 0.0 else None ,
                             value_3=float(m.dim4) if m.dim4 != 0.0 else None ,
                             )
        ids.update({m.id: n.pk})

    print(ids)

    definition = """
OLD DATABASE             NEW DATABASE
MasquesMasques             Mask
    actif                     active
    anneecre                  creationYear
    concepteur                conceptor
    description               description
    fabricant                 manufacturer
    fichiergds                GDSFile
    local                     localisation
    niveau                    level
    nom                       name
    num                       idNumber
    polarite                  polarisation
    usage                     usage
"""
    for ma in MasquesMasques().select():
        u=Usage.objects.get(name=ma.usage.nom)
        f=Manufacturer.objects.get(corporateName=ma.fabricant.rais_soc)
        l=Localisation.objects.get(localisation=ma.local.nom)
        na=ma.nom
        if Mask.objects.filter(name=na):
            na=na+"_1"
        nm=Mask.objects.create(condition='new' if ma.actif else 'broken',
                            creationYear=ma.anneecre,
                            conceptor=ma.concepteur,
                            description=ma.description,
                            manufacturer=f,
                            localisation=l,
                            level=ma.niveau,
                            name=na,
                            idNumber="%05d" % int(ma.num),
                            polarisation=ma.polarite,
                            usage=u)


        for i in ma.masquesmasquesmotif_set:
            n=("%s_%sx%s:%s" % (i.motifs.typemotif.nom,i.motifs.dim1,i.motifs.dim2,i.motifs.pas))
            #print(i.motifs_id,ids[i.motifs_id])
            print("\t",n,Motif.objects.get(id=ids[i.motifs_id]))
            nm.motifs.add(Motif.objects.get(id=ids[i.motifs_id]))

        for i in ma.masquesimage_set:

            image=Image(mask_id=nm.id)
            with open(MEDIA+i.image, 'rb') as doc_file:
                image.image.save(i.image,File(doc_file),save=True)
            print("\t",i.image)

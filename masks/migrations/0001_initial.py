# Generated by Django 2.0.2 on 2018-09-04 19:46

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor.fields.RichTextField(verbose_name='about')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/mask')),
            ],
        ),
        migrations.CreateModel(
            name='Localisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('localisation', models.CharField(max_length=100, verbose_name='Localisation')),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corporateName', models.CharField(max_length=100, verbose_name='Corporate Name')),
                ('address1', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Address')),
                ('address2', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Address')),
                ('postcode', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Postal Code')),
                ('city', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='City')),
                ('country', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Country')),
                ('email', models.EmailField(blank=True, default='', max_length=100, null=True, verbose_name='@mail')),
            ],
        ),
        migrations.CreateModel(
            name='Mask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('idNumber', models.CharField(default='', max_length=50, unique=True, verbose_name='id. number')),
                ('conceptor', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Conceptor')),
                ('level', models.IntegerField(default=1, verbose_name='Level')),
                ('creationYear', models.CharField(default='2000', max_length=10, verbose_name='year of creation')),
                ('GDSFile', models.FileField(blank=True, default='', null=True, upload_to='GDS/', verbose_name='GDS File')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('polarisation', models.CharField(choices=[('---', 'Select'), ('Positif', 'Positif'), ('Negatif', 'Negatif')], default='Select', max_length=20, verbose_name='Polarisation')),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='Description')),
                ('localisation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='first.Localisation')),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='first.Manufacturer')),
            ],
        ),
        migrations.CreateModel(
            name='Motif',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('step', models.FloatField(verbose_name='Step')),
                ('value0', models.FloatField()),
                ('value1', models.FloatField(blank=True, default=None, null=True)),
                ('value2', models.FloatField(blank=True, default=None, null=True)),
                ('value3', models.FloatField(blank=True, default=None, null=True)),
                ('value4', models.FloatField(blank=True, default=None, null=True)),
                ('value5', models.FloatField(blank=True, default=None, null=True)),
                ('value6', models.FloatField(blank=True, default=None, null=True)),
                ('value7', models.FloatField(blank=True, default=None, null=True)),
                ('value8', models.FloatField(blank=True, default=None, null=True)),
                ('value9', models.FloatField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MotifType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='something has to be written here', max_length=255, unique=True, verbose_name='name of the type of motif')),
                ('nb_parameters', models.IntegerField(verbose_name='the number of parameters')),
                ('parameters_data', models.CharField(max_length=2000)),
                ('comment', models.CharField(max_length=1000, verbose_name='Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Usage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Usage')),
                ('comment', models.CharField(max_length=1000, verbose_name='Comment')),
            ],
        ),
        migrations.AddField(
            model_name='motif',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first.MotifType'),
        ),
        migrations.AddField(
            model_name='mask',
            name='motifs',
            field=models.ManyToManyField(to='first.Motif'),
        ),
        migrations.AddField(
            model_name='mask',
            name='usage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='first.Usage'),
        ),
        migrations.AddField(
            model_name='image',
            name='mask',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first.Mask'),
        ),
    ]

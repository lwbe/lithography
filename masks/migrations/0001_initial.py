# Generated by Django 2.1.7 on 2019-03-21 10:35

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
                ('address2', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Address cpl.')),
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
                ('localisation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='masks.Localisation')),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='masks.Manufacturer')),
            ],
        ),
        migrations.CreateModel(
            name='Motif',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('step', models.FloatField(verbose_name='Step')),
                ('value_0', models.FloatField(verbose_name='First parameter')),
                ('value_1', models.FloatField(blank=True, null=True, verbose_name='Second parameter')),
                ('value_2', models.FloatField(blank=True, null=True, verbose_name='Third parameter')),
                ('value_3', models.FloatField(blank=True, null=True, verbose_name='Fourth parameter')),
                ('value_4', models.FloatField(blank=True, null=True, verbose_name='Fifth parameter')),
                ('value_5', models.FloatField(blank=True, null=True, verbose_name='Sixth parameter')),
                ('value_6', models.FloatField(blank=True, null=True, verbose_name='Seventh parameter')),
                ('value_7', models.FloatField(blank=True, null=True, verbose_name='Eight parameter')),
                ('value_8', models.FloatField(blank=True, null=True, verbose_name='Ninth parameter')),
                ('value_9', models.FloatField(blank=True, null=True, verbose_name='Tenth parameter')),
            ],
        ),
        migrations.CreateModel(
            name='MotifType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='something has to be written here', max_length=255, unique=True, verbose_name='name of the type of motif')),
                ('nb_parameters', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9')], default=1, verbose_name='the number of parameters')),
                ('param_name_0', models.CharField(max_length=255, verbose_name='First parameter name')),
                ('param_name_1', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Second parameter name')),
                ('param_name_2', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Third parameter name')),
                ('param_name_3', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Fourth parameter name')),
                ('param_name_4', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Fifth parameter name')),
                ('param_name_5', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Sixth parameter name')),
                ('param_name_6', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Seventh parameter name')),
                ('param_name_7', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Eighth parameter name')),
                ('param_name_8', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Ninth parameter name')),
                ('param_name_9', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Tenth parameter name')),
                ('comment', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Comment')),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='masks.MotifType'),
        ),
        migrations.AddField(
            model_name='mask',
            name='motifs',
            field=models.ManyToManyField(to='masks.Motif'),
        ),
        migrations.AddField(
            model_name='mask',
            name='usage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='masks.Usage'),
        ),
        migrations.AddField(
            model_name='image',
            name='mask',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='masks.Mask'),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-24 21:58

from django.db import migrations, models
import django_jsonform.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='english_names',
            field=django_jsonform.models.fields.ArrayField(base_field=models.CharField(max_length=255), size=None),
        ),
        migrations.AlterField(
            model_name='plant',
            name='halkomelem_names',
            field=django_jsonform.models.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), size=None, verbose_name='hən̓q̓əmin̓əm̓ names'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='squamish_names',
            field=django_jsonform.models.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), size=None, verbose_name='Sḵwx̱wú7mesh Sníchim label'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='western_scientific_names',
            field=django_jsonform.models.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), size=None),
        ),
    ]
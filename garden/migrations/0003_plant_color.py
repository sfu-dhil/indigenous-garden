# Generated by Django 4.2.7 on 2023-11-24 22:43

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0002_alter_plant_english_names_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='color',
            field=colorfield.fields.ColorField(default='#008000', image_field=None, max_length=25, samples=None),
        ),
    ]

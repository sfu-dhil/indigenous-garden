# Generated by Django 5.0.7 on 2024-08-27 19:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0003_remove_panoramapoint_feature_alter_englishname_audio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='feature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='points', to='garden.feature'),
        ),
        migrations.AlterModelTable(
            name='point',
            table='garden_point',
        ),
    ]

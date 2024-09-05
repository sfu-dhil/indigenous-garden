# Generated by Django 5.0.8 on 2024-09-05 03:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0005_feature_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='point',
            options={'ordering': ['-y', 'x']},
        ),
        migrations.RunSQL([
            ("UPDATE garden_point set y = y - 1510;")
        ]),
    ]

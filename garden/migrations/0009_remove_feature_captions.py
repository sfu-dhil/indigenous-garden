# Generated by Django 5.1.7 on 2025-03-27 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0008_feature_video_original_feature_video_thumbnail_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature',
            name='captions',
        ),
    ]

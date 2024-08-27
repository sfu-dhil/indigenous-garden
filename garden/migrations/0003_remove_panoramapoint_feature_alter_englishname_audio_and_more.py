# Generated by Django 5.0.7 on 2024-08-27 19:45

import django.db.models.deletion
import garden.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0002_remove_feature_audio_remove_image_thumbnail_height_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='panoramapoint',
            name='feature',
        ),
        migrations.AlterField(
            model_name='englishname',
            name='audio',
            field=garden.models.AsyncConstrainedFileField(blank=True, content_types=['application/octet-stream', 'audio/mpeg', 'audio/wav', 'audio/ogg'], help_text='Only MP3 (.mp3), WAV (.wav), or Ogg (.ogg) is allowed.', mime_lookup_length=4096, null=True, upload_to='audio/'),
        ),
        migrations.AlterField(
            model_name='feature',
            name='video',
            field=garden.models.AsyncConstrainedFileField(blank=True, content_types=['application/octet-stream', 'video/mp4', 'video/webm', 'video/ogg'], help_text='Only MP4 (.mp4), WebM (.webm), or Ogg (.ogv) is allowed.', mime_lookup_length=4096, null=True, upload_to='videos/'),
        ),
        migrations.AlterField(
            model_name='halkomelemname',
            name='audio',
            field=garden.models.AsyncConstrainedFileField(blank=True, content_types=['application/octet-stream', 'audio/mpeg', 'audio/wav', 'audio/ogg'], help_text='Only MP3 (.mp3), WAV (.wav), or Ogg (.ogg) is allowed.', mime_lookup_length=4096, null=True, upload_to='audio/'),
        ),
        migrations.AlterField(
            model_name='squamishname',
            name='audio',
            field=garden.models.AsyncConstrainedFileField(blank=True, content_types=['application/octet-stream', 'audio/mpeg', 'audio/wav', 'audio/ogg'], help_text='Only MP3 (.mp3), WAV (.wav), or Ogg (.ogg) is allowed.', mime_lookup_length=4096, null=True, upload_to='audio/'),
        ),
        migrations.AlterField(
            model_name='westernscientificname',
            name='audio',
            field=garden.models.AsyncConstrainedFileField(blank=True, content_types=['application/octet-stream', 'audio/mpeg', 'audio/wav', 'audio/ogg'], help_text='Only MP3 (.mp3), WAV (.wav), or Ogg (.ogg) is allowed.', mime_lookup_length=4096, null=True, upload_to='audio/'),
        ),
        migrations.RenameModel(
            old_name='OverheadPoint',
            new_name='Point',
        ),
        migrations.DeleteModel(
            name='PanoramaPoint',
        ),
    ]

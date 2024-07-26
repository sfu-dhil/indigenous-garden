# Generated by Django 5.0.3 on 2024-07-26 20:01

import django_advance_thumbnail.fields
import garden.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature',
            name='audio',
        ),
        migrations.RemoveField(
            model_name='image',
            name='thumbnail_height',
        ),
        migrations.RemoveField(
            model_name='image',
            name='thumbnail_width',
        ),
        migrations.AddField(
            model_name='feature',
            name='video',
            field=garden.models.AsyncConstrainedFileField(blank=True, content_types=['video/mp4', 'video/webm', 'video/ogg'], help_text='Only MP4 (.mp4), WebM (.webm), or Ogg (.ogv) is allowed.', mime_lookup_length=4096, null=True, upload_to='videos/'),
        ),
        migrations.AlterField(
            model_name='image',
            name='thumbnail',
            field=django_advance_thumbnail.fields.AdvanceThumbnailField(blank=True, null=True, upload_to='thumbnails/'),
        ),
        migrations.AlterField(
            model_name='englishname',
            name='audio',
            field=garden.models.AsyncConstrainedFileField(blank=True, content_types=['audio/mpeg', 'audio/wav', 'audio/ogg'], help_text='Only MP3 (.mp3), WAV (.wav), or Ogg (.ogg) is allowed.', mime_lookup_length=4096, null=True, upload_to='audio/'),
        ),
        migrations.AlterField(
            model_name='halkomelemname',
            name='audio',
            field=garden.models.AsyncConstrainedFileField(blank=True, content_types=['audio/mpeg', 'audio/wav', 'audio/ogg'], help_text='Only MP3 (.mp3), WAV (.wav), or Ogg (.ogg) is allowed.', mime_lookup_length=4096, null=True, upload_to='audio/'),
        ),
        migrations.AlterField(
            model_name='squamishname',
            name='audio',
            field=garden.models.AsyncConstrainedFileField(blank=True, content_types=['audio/mpeg', 'audio/wav', 'audio/ogg'], help_text='Only MP3 (.mp3), WAV (.wav), or Ogg (.ogg) is allowed.', mime_lookup_length=4096, null=True, upload_to='audio/'),
        ),
        migrations.AlterField(
            model_name='westernscientificname',
            name='audio',
            field=garden.models.AsyncConstrainedFileField(blank=True, content_types=['audio/mpeg', 'audio/wav', 'audio/ogg'], help_text='Only MP3 (.mp3), WAV (.wav), or Ogg (.ogg) is allowed.', mime_lookup_length=4096, null=True, upload_to='audio/'),
        ),
    ]
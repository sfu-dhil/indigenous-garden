# Generated by Django 5.1.3 on 2024-11-22 19:26

import constrainedfilefield.fields.file
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0006_alter_point_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='feature',
            name='references',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='feature',
            name='captions',
            field=constrainedfilefield.fields.file.ConstrainedFileField(blank=True, content_types=['text/vtt'], help_text='Only <u><a href="https://developer.mozilla.org/en-US/docs/Web/API/WebVTT_API" target="_blank">WebVTT (.vtt)</a></u> is allowed.', mime_lookup_length=4096, null=True, upload_to='captions/'),
        ),
        migrations.AlterField(
            model_name='feature',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(height_field='image_height', help_text='Please use <u><a href="https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types" target="_blank">standard web image types</a></u>. PNG, JPEG, and WebP are recommended.', upload_to='images/', width_field='image_width'),
        ),
    ]

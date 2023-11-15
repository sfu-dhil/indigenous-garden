from django.db import models
from safe_filefield.models import SafeFileField
from django_jsonform.models.fields import ArrayField
from colorfield.fields import ColorField

# models
class Plant(models.Model):
    # fields
    number = models.IntegerField(unique=True)
    color = ColorField(default='#008000')

    english_names = ArrayField(
        models.CharField(max_length=255),
    )
    english_names_audio = SafeFileField(
        verbose_name="English audio",
        upload_to='audio/',
        null=True,
        blank=True,
        allowed_extensions=['mp3', 'wav', 'ogg'],
        check_content_type=True,
    )
    english_content = models.TextField()
    english_content_audio = SafeFileField(
        verbose_name="English audio",
        upload_to='audio/',
        null=True,
        blank=True,
        allowed_extensions=['mp3', 'wav', 'ogg'],
        check_content_type=True,
    )

    western_scientific_names = ArrayField(
        models.CharField(max_length=255, blank=True),
    )
    western_scientific_names_audio = SafeFileField(
        verbose_name="Western scientific audio",
        upload_to='audio/',
        null=True,
        blank=True,
        allowed_extensions=['mp3', 'wav', 'ogg'],
        check_content_type=True,
    )

    halkomelem_names = ArrayField(
        models.CharField(max_length=255, blank=True),
        verbose_name="hən̓q̓əmin̓əm̓ names",
    )
    halkomelem_names_audio = SafeFileField(
        verbose_name="hən̓q̓əmin̓əm̓ audio",
        upload_to='audio/',
        null=True,
        blank=True,
        allowed_extensions=['mp3', 'wav', 'ogg'],
        check_content_type=True,
    )
    halkomelem_content = models.TextField(
        verbose_name="hən̓q̓əmin̓əm̓ content",
        blank=True,
    )
    halkomelem_content_audio = SafeFileField(
        verbose_name="hən̓q̓əmin̓əm̓ audio",
        upload_to='audio/',
        null=True,
        blank=True,
        allowed_extensions=['mp3', 'wav', 'ogg'],
        check_content_type=True,
    )

    squamish_names = ArrayField(
        models.CharField(max_length=255, blank=True),
        verbose_name="Sḵwx̱wú7mesh Sníchim label",
    )
    squamish_names_audio = SafeFileField(
        verbose_name="Sḵwx̱wú7mesh Sníchim audio",
        upload_to='audio/',
        null=True,
        blank=True,
        allowed_extensions=['mp3', 'wav', 'ogg'],
        check_content_type=True,
    )
    squamish_content = models.TextField(
        verbose_name="Sḵwx̱wú7mesh Sníchim content",
        blank=True,
    )
    squamish_content_audio = SafeFileField(
        verbose_name="Sḵwx̱wú7mesh Sníchim audio",
        upload_to='audio/',
        null=True,
        blank=True,
        allowed_extensions=['mp3', 'wav', 'ogg'],
        check_content_type=True,
    )

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'garden_plant'
        indexes = [
            models.Index(fields=['number']),
        ]

    def __str__(self):
        return f'{self.number} {self.english_names} / {self.western_scientific_names} / {self.halkomelem_names} / {self.squamish_names}'

class Image(models.Model):
    # relationships
    plant = models.ForeignKey(
        Plant,
        related_name='images',
        on_delete=models.CASCADE
    )

    # fields
    image = models.ImageField(
        upload_to='images/',
        null=True,
        blank=True,
        help_text='Upload an image or provide an image url. If both are present, only the image upload will be used',
    )
    image_url = models.URLField(
        null=True,
        blank=True,
    )
    image_license = models.TextField(blank=True)

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'garden_image'

class Point(models.Model):
    # relationships
    plant = models.ForeignKey(
        Plant,
        related_name='points',
        on_delete=models.CASCADE
    )

    # fields
    x = models.FloatField()
    y = models.FloatField()

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'garden_point'
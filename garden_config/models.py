from django.db import models
from django.utils.safestring import mark_safe
from solo.models import SingletonModel
from django_advance_thumbnail import AdvanceThumbnailField
from garden.models import AsyncConstrainedFileField
from django_jsonform.models.fields import ArrayField

# abstract Models

# Models (load order matters)
class WelcomePopup(SingletonModel):
    heading = models.CharField(default='Welcome to This Garden')
    heading_halkomelem = models.CharField(null=True, blank=True)
    heading_halkomelem_audio = AsyncConstrainedFileField(
        upload_to='audio/',
        null=True,
        blank=True,
        content_types=['application/octet-stream', 'audio/mpeg', 'audio/wav', 'audio/ogg'],
        help_text='Only MP3 (.mp3), WAV (.wav), or Ogg (.ogg) is allowed.',
    )
    heading_squamish = models.CharField(null=True, blank=True)
    heading_squamish_audio = AsyncConstrainedFileField(
        upload_to='audio/',
        null=True,
        blank=True,
        content_types=['application/octet-stream', 'audio/mpeg', 'audio/wav', 'audio/ogg'],
        help_text='Only MP3 (.mp3), WAV (.wav), or Ogg (.ogg) is allowed.',
    )
    image = models.ImageField(
        upload_to='images/',
        null=True,
        blank=True,
        help_text=mark_safe('Please use <u><a href="https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types" target="_blank">standard web image types</a></u>. PNG, JPEG, and WebP are recommended.'),
        verbose_name='Picture',
    )
    thumbnail = AdvanceThumbnailField(
        source_field='image',
        upload_to='thumbnails/',
        null=True,
        blank=True,
        size=(800, 450),
    )
    image_caption = models.CharField(null=True, blank=True, verbose_name='Picture Caption')
    content = models.TextField(null=True, blank=True)

    # relationships

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'garden_config_welcome_popup'
        verbose_name = 'Welcome Popup'

    def __str__(self):
        return 'Welcome Popup'

class History(SingletonModel):
    heading = models.CharField(default='History of the SFU Indigenous Garden')
    content_4 = models.TextField(verbose_name='Ground Breaking Ceremony Content', null=True, blank=True)
    content_1 = models.TextField(verbose_name='Introduction to History of the Garden Content', null=True, blank=True)
    content_2 = models.TextField(verbose_name='Design & Identifying the Plants Content', null=True, blank=True)
    content_3 = models.TextField(verbose_name='Usage of the Space Content', null=True, blank=True)
    content_5 = models.TextField(verbose_name='Future Goals, Directions and Dreams Content', null=True, blank=True)

    # relationships

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'garden_config_history'
        verbose_name = 'History'

    def __str__(self):
        return 'History'

class ResidentialSchools(SingletonModel):
    heading = models.CharField(default='Indian Residential Schools Map')
    image = models.ImageField(
        upload_to='images/',
        null=True,
        blank=True,
        help_text=mark_safe('Please use <u><a href="https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types" target="_blank">standard web image types</a></u>. PNG, JPEG, and WebP are recommended.'),
        verbose_name='Map Picture',
    )
    thumbnail = AdvanceThumbnailField(
        source_field='image',
        upload_to='thumbnails/',
        null=True,
        blank=True,
        size=(800, 450),
    )
    image_caption = models.CharField(verbose_name='Map Picture Caption', default='Residential Schools of Canada')
    content = models.TextField(null=True, blank=True)

    # relationships

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'garden_config_residential_schools'
        verbose_name = 'Indian Residential Schools Map'

    def __str__(self):
        return 'Indian Residential Schools Map'


class ContextualEthicalFraming(SingletonModel):
    heading = models.CharField(default='Contextual and Ethical Framing')
    content = models.TextField(null=True, blank=True)

    # relationships

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'garden_config_contextual_ethical_framing'
        verbose_name = 'Contextual and Ethical Framing'

    def __str__(self):
        return 'Contextual and Ethical Framing'


class RelationalInterconnectedTeachings(SingletonModel):
    heading = models.CharField(default='Relational and Interconnected Teachings')
    content = models.TextField(null=True, blank=True)

    # relationships

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'garden_config_relational_interconnected_teachings'
        verbose_name = 'Relational and Interconnected Teachings'

    def __str__(self):
        return 'Relational and Interconnected Teachings'

class Acknowledgements(SingletonModel):
    heading = models.CharField(default='Acknowledgements')
    content = models.TextField(null=True, blank=True)

    # relationships

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'garden_config_acknowledgements'
        verbose_name = 'Acknowledgements'

    def __str__(self):
        return 'Acknowledgements'


class AcknowledgementsContentBlock(models.Model):
    heading = models.CharField()
    list = ArrayField(models.CharField(max_length=None), blank=True)
    content = models.TextField(null=True, blank=True)
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        db_index=True,
    )

    # relationships
    acknowledgements = models.ForeignKey(
        Acknowledgements,
        related_name='content_blocks',
        on_delete=models.CASCADE,
    )

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'garden_config_acknowledgements_content_block'
        ordering = ['order']

    def __str__(self):
        return self.heading

class OverheadMap(SingletonModel):
    date = models.DateField(null=True, blank=True)

    # relationships

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'garden_config_overhead_map'
        verbose_name = 'Overhead Map'

    def __str__(self):
        return 'Overhead Map'


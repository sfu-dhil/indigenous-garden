from django.db import models
from safe_filefield.models import SafeFileField
from colorfield.fields import ColorField
from django_jsonform.models.fields import JSONField

# models
class Feature(models.Model):
    FEATURE_NAME_SCHEMA = {
        'type': 'array',
        'items': {
            'type': 'dict',
            'keys': {
                'name': {
                    'type': 'string',
                },
                'descriptor': {
                    'type': 'string',
                    'helpText': 'Optionally add a descriptor after the name like `bush`, `fruit`, `tree`, etc.'
                }
            },
            'required': ['name'],
        },
    }

    class FeatureTypes(models.TextChoices):
        PLANT = "PLANT", "Plant"
        FEATURE = "GARDEN_FEATURE", "Garden Feature"

    # fields
    number = models.IntegerField(unique=True)
    color = ColorField(default='#7cb341')
    feature_type = models.CharField(
        max_length=255,
        choices=FeatureTypes.choices,
        default=FeatureTypes.PLANT,
    )
    audio = SafeFileField(
        upload_to='audio/',
        null=True,
        blank=True,
        allowed_extensions=['mp3', 'wav', 'ogg'],
        check_content_type=True,
    )

    english_names = JSONField(
        schema=FEATURE_NAME_SCHEMA
    )
    western_scientific_names = JSONField(
        schema=FEATURE_NAME_SCHEMA,
        blank=True
    )
    halkomelem_names = JSONField(
        schema=FEATURE_NAME_SCHEMA,
        verbose_name="hən̓q̓əmin̓əm̓ names",
        blank=True
    )
    squamish_names = JSONField(
        schema=FEATURE_NAME_SCHEMA,
        verbose_name="Sḵwx̱wú7mesh Sníchim names",
        blank=True
    )
    content = models.TextField()

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'garden_feature'

    def __str__(self):
        return f'{self.number} {self.all_names_str()}'

    def _format_name(self, item_dict):
        return f"{item_dict['name']} ({item_dict['descriptor']})" if item_dict['descriptor'] else item_dict['name']

    def all_names_str(self):
        return ' / '.join([
            self._format_name(item) for item in self.english_names
        ] + [
            self._format_name(item) for item in self.western_scientific_names
        ] + [
            self._format_name(item) for item in self.halkomelem_names
        ] + [
            self._format_name(item) for item in self.squamish_names
        ])

class Image(models.Model):
    # relationships
    feature = models.ForeignKey(
        Feature,
        related_name='images',
        on_delete=models.CASCADE
    )

    # fields
    image = models.ImageField(
        upload_to='images/',
        null=True,
        blank=True,
        help_text='Upload an image or provide an image url. If both are present, only the uploaded image will be used',
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
        db_table = 'garden_feature_image'

class OverheadPoint(models.Model):
    # relationships
    feature = models.ForeignKey(
        Feature,
        related_name='overhead_points',
        on_delete=models.CASCADE,
    )

    # fields
    x = models.FloatField()
    y = models.FloatField()

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'garden_overhead_point'

class PanoramaPoint(models.Model):
    # relationships
    feature = models.ForeignKey(
        Feature,
        related_name='panorama_points',
        on_delete=models.CASCADE,
    )

    # fields
    yaw = models.FloatField() # x
    pitch = models.FloatField() # y

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'garden_panorama_point'
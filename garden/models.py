import PIL
from django.db import models
from constrainedfilefield.fields import ConstrainedFileField
from django_advance_thumbnail import AdvanceThumbnailField
from admin_async_upload.models import AsyncFileField
from django.utils.safestring import mark_safe

class AsyncConstrainedFileField(ConstrainedFileField, AsyncFileField):
    def formfield(self, **kwargs):
        formfield = super(AsyncConstrainedFileField, self).formfield(**kwargs)
        if self.js_checker:
            formfield.widget.attrs.update(
                {"onchange": "validateFileSize(this, 0, %d);" % (self.max_upload_size,)}
            )
        return formfield

# modal signals
def image_compressor(sender, **kwargs):
    if kwargs["created"]:
        with PIL.Image.open(kwargs["instance"].image.path) as image:
            image.save(kwargs["instance"].image.path, optimize=True, quality=80)

# models
class Feature(models.Model):
    class FeatureTypes(models.TextChoices):
        PLANT = "PLANT", "Plant"
        FEATURE = "GARDEN_FEATURE", "Garden Feature"

    # fields
    published = models.BooleanField(
        default=True,
    )
    feature_type = models.CharField(
        max_length=255,
        choices=FeatureTypes.choices,
        default=FeatureTypes.PLANT,
    )
    number = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
    )
    video = AsyncConstrainedFileField(
        upload_to='videos/',
        null=True,
        blank=True,
        content_types=['application/octet-stream', 'video/mp4', 'video/webm', 'video/ogg'],
        help_text='Only MP4 (.mp4), WebM (.webm), or Ogg (.ogv) is allowed.',
    )
    captions = ConstrainedFileField(
        upload_to='captions/',
        null=True,
        blank=True,
        content_types=['text/vtt'],
        help_text=mark_safe('Only <u><a href="https://developer.mozilla.org/en-US/docs/Web/API/WebVTT_API" target="_blank">WebVTT (.vtt)</a></u> is allowed.'),
    )
    content = models.TextField(
        null=True,
        blank=True,
    )
    references = models.TextField(
        null=True,
        blank=True,
    )

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'garden_feature'

    def __str__(self):
        return f'{self.number} {self.all_names_str()}'

    def all_names_str(self):
        return ' / '.join(
            [str(n) for n in self.english_names.all()] +
            [str(n) for n in self.western_scientific_names.all()] +
            [str(n) for n in self.halkomelem_names.all()] +
            [str(n) for n in self.squamish_names.all()]
        )

class Name(models.Model):
    # fields
    name = models.CharField(
        max_length=255
    )
    descriptor = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    audio = AsyncConstrainedFileField(
        upload_to='audio/',
        null=True,
        blank=True,
        content_types=['application/octet-stream', 'audio/mpeg', 'audio/wav', 'audio/ogg'],
        help_text='Only MP3 (.mp3), WAV (.wav), or Ogg (.ogg) is allowed.',
    )

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name} ({self.descriptor})" if self.descriptor else self.name

class EnglishName(Name):
    # relationships
    feature = models.ForeignKey(
        Feature,
        related_name='english_names',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'garden_feature_english_name'

class WesternScientificName(Name):
    # relationships
    feature = models.ForeignKey(
        Feature,
        related_name='western_scientific_names',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'garden_feature_western_scientific_name'

class HalkomelemName(Name):
    # relationships
    feature = models.ForeignKey(
        Feature,
        related_name='halkomelem_names',
        on_delete=models.CASCADE
    )

    # relationships
    class Meta:
        db_table = 'garden_feature_halkomelem_name'

class SquamishName(Name):
    # relationships
    feature = models.ForeignKey(
        Feature,
        related_name='squamish_names',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'garden_feature_squamish_name'

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
        width_field='image_width',
        height_field='image_height',
        help_text=mark_safe('Please use <u><a href="https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types" target="_blank">standard web image types</a></u>. PNG, JPEG, and WebP are recommended.'),
    )
    image_width = models.IntegerField(
        null=True,
        blank=True,
    )
    image_height = models.IntegerField(
        null=True,
        blank=True,
    )

    thumbnail = AdvanceThumbnailField(
        source_field='image',
        upload_to='thumbnails/',
        null=True,
        blank=True,
        size=(520, 520),
    )

    description = models.TextField(
        null=True,
        blank=True,
        help_text='Description of the image for accessibility.',
    )
    license = models.TextField(
        null=True,
        blank=True,
    )

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'garden_feature_image'

    def __str__(self):
        return self.image.name if self.image else self.id
models.signals.post_save.connect(image_compressor, sender=Image)

class Point(models.Model):
    # relationships
    feature = models.ForeignKey(
        Feature,
        related_name='points',
        on_delete=models.CASCADE,
    )

    # fields
    x = models.FloatField()
    y = models.FloatField()

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'garden_point'
        ordering = ['-y', 'x']

    def __str__(self):
        return f"Map point: ({self.x:.2f},{self.y:.2f}) for {self.feature}"
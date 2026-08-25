from django.db import models
from django.utils.safestring import mark_safe
from pathlib import Path
from django.db.models import Q
from solo.models import SingletonModel

from django_dh_map.models import ContentItem, ContentBlock, Map, XyzMap, OverheadImageMap, PanoramaImageMap
from django_dh_map.settings import MEDIA_ROOT_DIR
from django_dh_map.fields import AsyncFFileField

class WelcomeModal(SingletonModel):
    title = models.CharField(default='Welcome')
    display = models.BooleanField(verbose_name='Display?', default=False, db_index=True)
    close_button_label = models.CharField(default='Close')

    # relationships
    # one-to-one content_item via WelcomeModalContent Model

    class Meta:
        db_table = 'indigenous_garden_app_welcome_modal'
        verbose_name = 'Welcome Modal'

    def __str__(self):
        return f'{self.title}'

class WelcomeModalContent(ContentItem):
    # relationships
    welcome_modal = models.OneToOneField(
        WelcomeModal,
        related_name='content_item',
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'indigenous_garden_app_ci_welcome_modal'
        verbose_name = 'Welcome Modal Content'

class ContentBlockMultilingualLabels(ContentBlock):
    # relationships
    # labels via the ContentBlockMultilingualLabel Model

    class Meta:
        db_table = 'indigenous_garden_app_cb_multilingual_labels'
        verbose_name = 'Multilingual Labels'
        ordering = ['position']

class ContentBlockMultilingualLabel(models.Model):
    class Language(models.TextChoices):
        ENGLISH = 'english', 'English'
        WESTERN_SCIENTIFIC = 'western_scientific', 'Western Scientific'
        HALKOMELEM = 'halkomelem', 'hən̓q̓əmin̓əm̓' #mark_safe('<span class="first-nations-unicode">hən̓q̓əmin̓əm̓</span>')
        SQUAMISH = 'squamish', 'Sḵwx̱wú7mesh Sníchim' #mark_safe('<span class="first-nations-unicode">Sḵwx̱wú7mesh Sníchim</span>')

    # fields
    position = models.IntegerField(default=0, db_index=True)
    language = models.CharField(choices=Language.choices)
    label = models.CharField(
        max_length=255
    )
    descriptor = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    original = AsyncFFileField(
        verbose_name='High Quality Audio',
        max_length=255,
        upload_to='audio/',
        help_text=mark_safe('Please use a high quality audio.'),
        # allowd_types=['jpeg', 'png', 'webp', 'avif'],
        null=True,
        blank=True
    )
    audio_dir = models.FilePathField(
        max_length=255,
        null=True,
        blank=True,
        path=(MEDIA_ROOT_DIR / 'audio/'),
        allow_folders=True,
        allow_files=False,
        recursive=False,
        match='label_audio_.*$',
    )
    audio = models.FileField(
        upload_to='audio/',
        null=True,
        blank=True,
    )

    # relationships
    multilingual_labels = models.ForeignKey(
        ContentBlockMultilingualLabels,
        related_name='labels',
        on_delete=models.CASCADE,
    )

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'indigenous_garden_app_cb_multilingual_label'
        verbose_name = 'Label'
        ordering = ['position']

    def save(self, *args, **kwargs):
        if not self.pk and not self.position:
            self.position = (ContentBlockMultilingualLabel.objects.aggregate(models.Max('position'))['position__max'] or 0 ) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.label} ({self.descriptor})" if self.descriptor else self.label

    def has_original(self):
        return bool(self.original.name) and self.original.storage.exists(self.original.name)

    def has_audio_dir(self):
        return bool(self.audio_dir) and Path(self.audio_dir).exists() and Path(self.audio_dir).is_dir() and len(list(Path(self.audio_dir).iterdir())) > 0

    def has_audio(self):
        return bool(self.audio.name) and self.audio.storage.exists(self.audio.name)
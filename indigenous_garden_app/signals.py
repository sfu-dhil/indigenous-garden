from django_rq import enqueue
from pathlib import Path
from django.db.models.signals import post_delete, post_init, post_save
from django.dispatch import receiver

from .models import ContentBlockMultilingualLabel
from django_dh_map.helpers import cleanup_directory
from .tasks import task_audio_label_stream_generator

@receiver(post_init, sender=ContentBlockMultilingualLabel)
def audio_post_init(sender, instance, **kwargs):
    instance.old_original_path = instance.original.path if instance.has_original() else None

@receiver(post_delete, sender=ContentBlockMultilingualLabel)
def audio_post_delete(sender, instance, **kwargs):
    audio_dir = Path(instance.audio_dir) if instance.audio_dir else None
    cleanup_directory(audio_dir)

@receiver(post_save, sender=ContentBlockMultilingualLabel)
def audio_post_save(sender, instance, **kwargs):
    original_path = instance.original.path if instance.has_original() else None
    has_new_audio = original_path and original_path != instance.old_original_path

    if has_new_audio:
        enqueue(task_audio_label_stream_generator, instance.pk)
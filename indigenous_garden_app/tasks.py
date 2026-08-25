import subprocess
from pathlib import Path
from django_dh_map.settings import MEDIA_ROOT_DIR, DH_MAP_FFMPEG
from django_dh_map.helpers import cleanup_directory, chown_directory
from django_rq import job

from .models import ContentBlockMultilingualLabel

# mostly copy+pasting django_dh_map.tasks task_audio_stream_generator and modifying for label's audio
@job('default', timeout=(60 * 20))
def task_audio_label_stream_generator(object_pk):
    cb_multilingual_label = ContentBlockMultilingualLabel.objects.get(pk=object_pk)

    if cb_multilingual_label.has_original():
        original_path = Path(cb_multilingual_label.original.path)

        audio_dir = MEDIA_ROOT_DIR / 'audio' / f'label_audio_{cb_multilingual_label.pk}'
        cleanup_directory(audio_dir)
        audio_dir.mkdir(parents=True, exist_ok=True)
        audio_stream_path = audio_dir / 'stream.ogg'

        # use ffmpeg to generate audio file (uses silenceremove filter to trims opening and closing silence)
        subprocess.run(
f'''{DH_MAP_FFMPEG} -i {original_path.absolute()}
-af "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.1:detection=peak,areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.1:detection=peak,areverse"
-c:a libopus -b:a 256k
{audio_stream_path.absolute()}'''.replace('\n', ' '),
            shell=True, check=True, capture_output=True, timeout=(60 * 15)
        )

        chown_directory(audio_dir)
        cb_multilingual_label.audio_dir = audio_dir
        cb_multilingual_label.audio.name = f'{audio_stream_path.relative_to(MEDIA_ROOT_DIR)}'
        cb_multilingual_label.save()
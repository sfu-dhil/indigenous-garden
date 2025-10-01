import PIL
import os
import PIL.Image
import math
from natsort import natsorted
from pathlib import Path
from ffmpeg import FFmpeg
from garden_app.settings import MEDIA_ROOT, MEDIA_URL, MEDIA_FOLDER_UID, MEDIA_FOLDER_GID

from .models import Feature, Image

def task_image_compressor(object_pk):
    image = Image.objects.get(pk=object_pk)
    with PIL.Image.open(image.image.path) as image_file:
        image_file.save(image.image.path, optimize=True, quality=80)

def task_video_thumbnail_generator(object_pk):
    feature = Feature.objects.get(pk=object_pk)

    has_original = bool(feature.video_original.name) and feature.video_original.storage.exists(feature.video_original.name)
    if has_original:
        original_file = Path(feature.video_original.path)
        media_dir = Path(MEDIA_ROOT)
        thumbnail_path = media_dir / 'thumbnails' / f'{Path(original_file).name}.png'

        if thumbnail_path.exists() and thumbnail_path.is_file:
            thumbnail_path.unlink(missing_ok=True)

        ffmpeg = FFmpeg() \
            .input(Path(original_file).absolute()) \
            .output(
                f'{thumbnail_path.absolute()}',
                {
                    'filter:v': 'thumbnail=300',
                    'frames:v': 1,
                }
            )
        ffmpeg.execute()

        feature.video_thumbnail.name = f'{(thumbnail_path).relative_to(Path(media_dir))}'
        feature.save()

def task_video_dash_generator(object_pk):
    feature = Feature.objects.get(pk=object_pk)

    has_original = bool(feature.video_original.name) and feature.video_original.storage.exists(feature.video_original.name)
    if has_original:
        original_file = Path(feature.video_original.path)
        media_dir = Path(MEDIA_ROOT)
        out_dir = media_dir / 'videos' / f'{feature.pk}'
        out_path = out_dir /  f'{Path(original_file).stem}.mpd'

        # remove existing
        feature.cleanup_extra_video_files()

        # create new folder
        out_dir.mkdir(parents=True, exist_ok=True)
        os.chown(out_dir.absolute(), MEDIA_FOLDER_UID, MEDIA_FOLDER_GID)

        ffmpeg = FFmpeg() \
            .input(Path(original_file).absolute()) \
            .output(
                f'{out_path.absolute()}',
                {
                    'map': ['0:v:0', '0:a:0', '0:v:0', '0:a:0', '0:v:0', '0:a:0'],
                    'c:v': 'libsvtav1',
                    # 'c:v': 'libx264',
                    'c:a': 'aac',

                    # 360p
                    'filter:v:0': 'scale=w=640:h=360',
                    # 'maxrate:v:0': '1498k',
                    'b:v:0': '1400k',
                    'b:a:0': '96k',

                    # 720p
                    'filter:v:1': 'scale=w=1280:h=720',
                    # 'maxrate:v:1': '2996k',
                    'b:v:1': '2800k',
                    'b:a:1': '128k',

                    # 1080p
                    'filter:v:2': 'scale=w=1920:h=1080',
                    # 'maxrate:v:2': '5350k',
                    'b:v:2': '5000k',
                    'b:a:2': '192k',

                    # 'dash_segment_type': 'webm',
                    'adaptation_sets': 'id=0,streams=v id=1,streams=a',
                    'f': 'dash',
                }
            )
        ffmpeg.execute()

        feature.video.name = f'{(out_path).relative_to(Path(media_dir))}'
        feature.save()

def task_video_hls_generator(object_pk):
    feature = Feature.objects.get(pk=object_pk)

    has_original = bool(feature.video_original.name) and feature.video_original.storage.exists(feature.video_original.name)
    if has_original:
        original_file = Path(feature.video_original.path)
        media_dir = Path(MEDIA_ROOT)
        out_dir = media_dir / 'videos' / f'{feature.pk}'
        master_pl_name = f'{Path(original_file).stem}.m3u8'

        feature.cleanup_extra_video_files()

        # create new folder
        out_dir.mkdir(parents=True, exist_ok=True)
        os.chown(out_dir.absolute(), MEDIA_FOLDER_UID, MEDIA_FOLDER_GID)

        ffmpeg = FFmpeg() \
            .input(Path(original_file).absolute()) \
            .output(
                f'{out_dir.absolute()}/%v.m3u8',
                {
                    'map': ['0:v:0', '0:a:0', '0:v:0', '0:a:0', '0:v:0', '0:a:0'],
                    'c:v': 'libx264',
                    'c:a': 'aac',

                    # 360p
                    'filter:v:0': 'scale=w=640:h=360',
                    'maxrate:v:0': '1498k',
                    'b:v:0': '1400k',
                    'b:a:0': '96k',

                    # 720p
                    'filter:v:1': 'scale=w=1280:h=720',
                    'maxrate:v:1': '2996k',
                    'b:v:1': '2800k',
                    'b:a:1': '128k',

                    # 1080p
                    'filter:v:2': 'scale=w=1920:h=1080',
                    'maxrate:v:2': '5350k',
                    'b:v:2': '5000k',
                    'b:a:2': '192k',

                    'var_stream_map': 'v:0,a:0,name:360p v:1,a:1,name:720p v:2,a:2,name:1080p',
                    'preset': 'fast',
                    'f': 'hls',
                    'hls_time': 5,
                    'hls_playlist_type': 'vod',
                    'hls_segment_type': 'mpegts',
                    'hls_flags': 'independent_segments',
                    'hls_segment_filename': f'{out_dir.absolute()}/%v_%03d.ts',
                    'master_pl_name': master_pl_name,
                }
            )
        ffmpeg.execute()

        feature.video.name = f'{(out_dir / master_pl_name).relative_to(Path(media_dir))}'
        feature.save()

def task_video_thumbnails_vtt_generator(object_pk):
    THUMBNAIL_INTERVAL = 2 # in seconds
    feature = Feature.objects.get(pk=object_pk)

    has_original = bool(feature.video_original.name) and feature.video_original.storage.exists(feature.video_original.name)
    if has_original:
        original_file = Path(feature.video_original.path)
        media_dir = Path(MEDIA_ROOT)
        out_dir = media_dir / 'thumbnails' / f'{feature.pk}'
        vtt_file = out_dir / 'thumbnails.vtt'
        storyboard_file = out_dir / 'storyboard.jpg'

        # remove existing
        feature.cleanup_extra_thumbnail_files()

        # create new folder
        out_dir.mkdir(parents=True, exist_ok=True)
        os.chown(out_dir.absolute(), MEDIA_FOLDER_UID, MEDIA_FOLDER_GID)

        ffmpeg = FFmpeg() \
            .input(Path(original_file).absolute()) \
            .output(
                f'{out_dir.absolute()}/storyboard_%d.jpg',
                {
                    'filter:v': f'fps=1/{THUMBNAIL_INTERVAL},scale=178:100',
                }
            )
        ffmpeg.execute()

        files = natsorted(list(out_dir.glob('*')))
        total_files = len(files)
        if total_files > 0:
            with open(vtt_file.absolute(), 'w') as f:
                f.write('WEBVTT\n\n')
                width, height = 0, 0
                with PIL.Image.open(files[0].absolute()) as first_image_file:
                    width, height = first_image_file.width, first_image_file.height
                total_width, total_height = width * (10 if total_files >= 10 else total_files), height * math.ceil(total_files / 10.0)

                storyboard_image = PIL.Image.new('RGB', size=(total_width, total_height))
                storyboard_image_url = Path(MEDIA_URL) / storyboard_file.relative_to(media_dir)

                for index, file in enumerate(files):
                    with PIL.Image.open(file.absolute()) as image_file:
                        w_index, h_index = width * (index % 10), height * math.floor(index / 10)
                        storyboard_image.paste(image_file, box=(w_index, h_index))

                        start_time = index * THUMBNAIL_INTERVAL
                        end_time = (index + 1) * THUMBNAIL_INTERVAL
                        start_time_str = f'{start_time//3600:02d}:{(start_time//60)%60:02d}:{start_time%60:06.3f}'
                        end_time_str = f'{end_time//3600:02d}:{(end_time//60)%60:02d}:{end_time%60:06.3f}'
                        f.write(f'{start_time_str} --> {end_time_str}\n')
                        f.write(f'/{storyboard_image_url}#xywh={w_index},{h_index},{width},{height}\n\n')
                    # remove storyboard segment
                    file.unlink(missing_ok=True)
                storyboard_image.save(storyboard_file)

        feature.video_thumbnails_vtt.name = f'{vtt_file.relative_to(Path(media_dir))}'
        feature.save()

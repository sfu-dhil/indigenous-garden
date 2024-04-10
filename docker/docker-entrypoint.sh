#!/bin/sh
set -e

# app specific setup here
python manage.py migrate

# collect static if needed
python manage.py collectstatic --noinput

export GIT_COMMIT=$(git rev-parse HEAD)
export GIT_COMMIT_SHORT=$(git rev-parse --short HEAD)
export GIT_BRANCH=$(git branch --show-current)
export GIT_TAG=$(git tag --points-at HEAD | head -n 1)

# fix media folder permissions for nginx
MEDIA_FOLDER_UID=${MEDIA_FOLDER_UID-101}
MEDIA_FOLDER_GID=${MEDIA_FOLDER_GID-101}
mkdir -p /media/audio /media/captions /media/images /media/thumbnails
chown $MEDIA_FOLDER_UID:$MEDIA_FOLDER_GID /media /media/audio /media/captions /media/images /media/thumbnails

python manage.py runserver 0.0.0.0:80
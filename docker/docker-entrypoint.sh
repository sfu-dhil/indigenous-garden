#!/bin/sh
set -e

# app specific setup here
python manage.py migrate

export GIT_COMMIT=$(git rev-parse HEAD)
export GIT_COMMIT_SHORT=$(git rev-parse --short HEAD)
export GIT_BRANCH=$(git branch --show-current)
export GIT_TAG=$(git tag --points-at HEAD | head -n 1)

python manage.py runserver 0.0.0.0:80
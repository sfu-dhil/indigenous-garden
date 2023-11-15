# Node deps
FROM node:20.4 AS indigenous-garden-prod-assets
WORKDIR /app

RUN npm upgrade -g npm \
    && npm upgrade -g yarn \
    && rm -rf /var/lib/apt/lists/*

# build js deps
COPY package.json yarn.lock /app/
RUN yarn --production \
    && yarn cache clean


# Django app
FROM python:3.11-alpine as indigenous-garden
EXPOSE 80
WORKDIR /app

# add system deps
RUN apk update \
    && apk add git libmagic \
    && pip install --no-cache-dir --upgrade pip \
    && rm -rf /var/cache/apk/*

# install python deps
COPY requirements.txt /app
RUN pip install -r requirements.txt --no-cache-dir

# add project files
COPY . /app

# add prod assets
COPY --from=indigenous-garden-prod-assets /app/node_modules /app/node_modules

# collect static assets for production
RUN python manage.py collectstatic --noinput

# run migrations and start server
CMD ["docker/docker-entrypoint.sh"]
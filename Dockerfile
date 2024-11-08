# Node deps
FROM node:23.1-slim AS indigenous-garden-vite
WORKDIR /app

RUN npm upgrade -g npm \
    && npm upgrade -g yarn \
    && rm -rf /var/lib/apt/lists/*

# build js deps
COPY garden_vite/package.json garden_vite/yarn.lock /app/
RUN yarn

# run vite build
COPY garden_vite /app
RUN yarn build

FROM indigenous-garden-vite AS indigenous-garden-vite-prod
RUN yarn --production \
    && yarn cache clean

# Django app
FROM python:3.11-alpine AS indigenous-garden
EXPOSE 80
WORKDIR /app

# add system deps
RUN apk update \
    && apk add git libmagic curl \
    && pip install --no-cache-dir --upgrade pip \
    && rm -rf /var/cache/apk/*

# install python deps
COPY requirements.txt /app
RUN pip install -r requirements.txt --no-cache-dir

# add project files
COPY . /app

# add prod assets
COPY --from=indigenous-garden-vite-prod /app/dist /static-vite/dist

# collect static assets for production
RUN python manage.py collectstatic --noinput

# run migrations and start server
CMD ["docker/docker-entrypoint.sh"]
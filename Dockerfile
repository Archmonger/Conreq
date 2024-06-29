# FROM ghcr.io/linuxserver/baseimage-alpine:3.20
FROM python:3.11.9-alpine3.20

ENV DATA_DIR=/config DEBUG=False

COPY ./manage.py /app/manage.py
COPY ./VERSION /app/VERSION
COPY ./LICENSE /app/LICENSE
COPY ./conreq/ /app/conreq/
COPY ./requirements/ /app/conreq/requirements/

RUN \
    echo "**** Install build dependencies ****" \
    && \
    apk add --no-cache --virtual=build-dependencies \
    bsd-compat-headers \
    build-base \
    cargo \
    curl \
    g++ \
    gcc \
    git \
    jq \
    libev-dev \
    libffi-dev \
    openssl-dev \
    && \
    echo "**** Install Linux packages ****" \
    && \
    apk add --no-cache \
    freetype-dev \
    fribidi-dev \
    harfbuzz-dev \
    jpeg-dev \
    lcms2-dev \
    openjpeg-dev \
    tcl-dev \
    tiff-dev \
    tk-dev \
    zlib-dev \
    && \
    echo "**** Install Python dependencies ****" \
    && \
    pip3 install --no-cache-dir -U -r /app/conreq/requirements/main.txt \
    && \
    echo "**** Cleanup ****" \
    && \
    apk del --purge \
    build-dependencies \
    && \
    rm -rf \
    /root/.cache \
    /root/.cargo \
    /tmp/*

EXPOSE 8000

WORKDIR /app/
CMD ["sh", "-c", "python3 manage.py run_conreq --uid ${PUID:=1000} --gid ${PGID:=1000}"]

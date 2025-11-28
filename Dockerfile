# BUILD COMMAND:
#   docker build . --no-cache -t conreq
#   mkdir config
# RUN COMMAND (Windows):
#   docker run -p '7575:7575/tcp' -v $PWD/config:/config conreq
# RUN COMMAND (Linux/Mac):
#   docker run -p '7575:7575/tcp' -v $(pwd)/config:/config conreq
FROM python:3.12.12-alpine3.21

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
    pip3 install uv \
    && \
    uv pip install --system --no-cache-dir -U -r /app/conreq/requirements/main.txt \
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

EXPOSE 7575

WORKDIR /app/
CMD ["sh", "-c", "python3 manage.py run_conreq --uid ${PUID:=99} --gid ${PGID:=100}"]

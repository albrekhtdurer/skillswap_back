FROM python:3.10-alpine

ENV APP /opt/skillswap_back
WORKDIR $APP
RUN apk add --no-cache gcc \
                       make \
                       musl-dev \
                       curl \
                       zlib \
                       zlib-dev \
                       sqlite

WORKDIR /tmp
COPY ./requirements.txt  /tmp/
RUN pip3 install --no-cache-dir --upgrade -r /tmp/requirements.txt
WORKDIR $APP

COPY . $APP

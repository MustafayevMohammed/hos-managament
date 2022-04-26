FROM python:3.9.6-alpine
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt requirements.txt
# RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev 

RUN pip3 install --upgrade pip
RUN apk add python3-dev libffi-dev libressl-dev libuv-dev build-base
# RUN pip3 install libffi-dev
RUN pip3 install -r requirements.txt
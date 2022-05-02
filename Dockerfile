FROM python:3.9.6-alpine
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt requirements.txt
# RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev 

# RUN pip3 install --upgrade pip && \
#     apk add python3-dev libffi-dev libressl-dev libuv-dev build-base && \
#     pip3 install -r requirements.txt && \
#     adduser --disabled-password --no-create-home app && \
#     mkdir -p /vol/web/static && \
#     mkdir -p /vol/web/media && \
#     chown -R app:app /vol && \
#     chmod -R 755 /vol
    
RUN pip3 install --upgrade pip
RUN apk add python3-dev libffi-dev libressl-dev libuv-dev build-base
RUN pip3 install -r requirements.txt
RUN adduser --disabled-password --no-create-home app
RUN mkdir -p /vol/web/static
RUN mkdir -p /vol/web/media
RUN chown -R app:app /vol
RUN chmod -R 755 /vol

USER app
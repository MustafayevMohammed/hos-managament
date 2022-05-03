FROM python:3.9.6-alpine
WORKDIR /app

ENV PATH="/scripts:${PATH}"
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
# RUN systemctl start docker
RUN apk add python3-dev libffi-dev libressl-dev libuv-dev build-base
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r requirements.txt
RUN apk del .tmp

# COPY ./scripts /scripts

# RUN chmod +x /scripts/*

# RUN mkdir -p /vol/web/media
# RUN mkdir -p /vol/web/static
# RUN adduser -D user
# RUN chown -R user:user /vol
# RUN chmod -R 755 /vol/web
# USER user
COPY ./entrypoint.sh /

ENTRYPOINT ["sh" ,"./entrypoint.sh" ]
# CMD ["entrypoint.sh"]
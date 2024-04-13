FROM python:3.10-alpine

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN apk update && \
    apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev \
    git bash

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --root-user-action=ignore

COPY . .
EXPOSE 8000
CMD ["sh", "entrypoint.sh"]
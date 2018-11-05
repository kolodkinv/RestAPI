FROM python:2.7

RUN useradd -u 1000 -m -s /bin/bash cm

RUN mkdir /code && chown cm:cm /code

USER cm
WORKDIR /code
COPY requirements.txt /code

USER root
RUN pip install -U pip
RUN pip install -r /code/requirements.txt

COPY . /code

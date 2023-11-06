FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /produccion
WORKDIR /produccion

COPY . /produccion/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt



# Dockerfile

FROM python:3.9
FROM postgres:14.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY . /app/

# Instala las dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x /app/credencial.zip



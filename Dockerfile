# Dockerfile

FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app


# Instala las dependencias incluyendo gunicorn
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/
RUN chmod 777 /app/init-db.sh
RUN chmod +x /app/credencial.zip



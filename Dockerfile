FROM postgres:14.9

RUN apt-get update && apt-get install -y python3 python3-pip

ENV PYTHONUNBUFFERED 1

RUN mkdir /produccion
WORKDIR /produccion

COPY . /produccion/

# Instala las dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x /app/credencial.zip



#!/bin/bash

./inicio.sh
unzip -o credencial.zip
python manage.py makemigrations roles login kanban administracion publicaciones
python manage.py migrate
python poblacion/poblar.py
gunicorn cms.wsgi:application --bind 0.0.0.0:8000

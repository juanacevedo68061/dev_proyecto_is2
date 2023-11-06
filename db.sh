#!/bin/bash

python manage.py makemigrations roles login kanban administracion publicaciones
python manage.py migrate
python poblacion/poblar.py

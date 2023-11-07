#!/bin/bash

until pg_isready -h db -p 5432 -U postgres
do
    echo "Esperando a que la base de datos esté disponible..."
    sleep 2
done &

python manage.py makemigrations roles login kanban administracion publicaciones
python manage.py migrate
python poblacion/poblar.py

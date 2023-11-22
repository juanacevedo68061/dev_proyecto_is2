@echo off

:: Crear un entorno virtual
python -m venv virtual

:: Activar el entorno virtual
call virtual\Scripts\activate
python -m pip install --upgrade pip
pip cache purge


:: Instalar las dependencias del proyecto desde el archivo requirements.txt
pip install -r requirements.txt

:: Realizar migraciones en la base de datos
python manage.py makemigrations roles login kanban administracion publicaciones
python manage.py migrate
python poblacion/poblar.py
python manage.py runserver

:: Mensaje de finalización
echo Configuración y migraciones completadas.

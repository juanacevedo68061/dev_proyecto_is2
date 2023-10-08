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
python manage.py makemigrations administracion 
python manage.py makemigrations roles
python manage.py makemigrations cms 
python manage.py makemigrations login
python manage.py makemigrations publicaciones
python manage.py migrate

:: Mensaje de finalización
echo Configuración y migraciones completadas.

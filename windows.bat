@echo off

:: Crear un entorno virtual
python -m venv virtual
python -m pip install --upgrade pip
:: Activar el entorno virtual
call virtual\Scripts\activate

:: Instalar las dependencias del proyecto desde el archivo requirements.txt
pip install -r requirements.txt

:: Realizar migraciones en la base de datos
python manage.py makemigrations canvan publicaciones administracion roles cms login
python manage.py migrate

:: Mensaje de finalización
echo Configuración y migraciones completadas.

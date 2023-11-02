import os

# Poblar la base de datos
os.system("python poblacion/poblar.py")

# Iniciar el servidor de desarrollo de Django
os.system("python manage.py runserver")

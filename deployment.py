import os

# Ejecutar los scripts de carga en orden
os.system("python carga_usuarios.py")
os.system("python carga_categorias.py")
os.system("python carga_publicaciones.py")

# Iniciar el servidor de desarrollo de Django
os.system("python manage.py runserver")

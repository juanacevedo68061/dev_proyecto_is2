import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms.settings')
django.setup()

from django.contrib.auth import login
from login.forms import FormularioRegistro
from login.models import Usuario

def cargar_usuarios():
    """
    Registra usuarios utilizando la vista de registro existente.

    Esta función utiliza la vista de registro de la aplicación para registrar usuarios
    utilizando datos proporcionados en un archivo JSON. Asegura que los signals de Django
    se activen para crear roles y asignar permisos.

    Retorna:
        int: El número de usuarios registrados con éxito.
    """
    try:
        ruta_json = 'login/data/usuarios.json'

        with open(ruta_json, 'r') as json_file:
            usuarios_data = json.load(json_file)

        usuarios_registrados = 0

        for usuario_data in usuarios_data:
            username = usuario_data['username']
            email = usuario_data['email']
            password = usuario_data['password1']

            usuario, creado = Usuario.objects.get_or_create(username=username, email=email)
            usuario.set_password(password)
            usuario.save()

            usuarios_registrados += 1

        print(f"Usuarios registrados con éxito: {usuarios_registrados}")
        return usuarios_registrados
    except FileNotFoundError:
        print(f"El archivo JSON no se encuentra en la ruta especificada: {ruta_json}")
        return 0
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")
        return 0

if __name__ == '__main__':
    cargar_usuarios()



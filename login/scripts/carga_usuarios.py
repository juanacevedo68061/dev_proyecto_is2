# login/scripts/carga_usuarios.py

import json
from django.contrib.auth.hashers import make_password
from login.models import Usuario  # Asegúrate de importar la clase Usuario desde tu aplicación

def cargar_usuarios(ruta_json):
    """
    Carga usuarios desde un archivo JSON y los registra en la base de datos.

    Esta función carga usuarios desde un archivo JSON especificado y crea las instancias
    de Usuario en la base de datos utilizando los datos proporcionados en el archivo.

    Parametros:
        ruta_json (str): La ruta al archivo JSON de usuarios.

    Retorna:
        int: El número de usuarios creados con éxito.
    """
    try:
        with open(ruta_json, 'r') as json_file:
            usuarios_data = json.load(json_file)

        usuarios_a_crear = []
        usuarios_creados = 0

        for usuario_data in usuarios_data:
            username = usuario_data['username']
            email = usuario_data['email']
            password1 = usuario_data['password1']
            password2 = usuario_data['password2']

            # Verifica que las contraseñas coincidan antes de crear el usuario
            if password1 == password2:
                usuario = Usuario(
                    username=username,
                    email=email,
                    password=make_password(password1)
                )
                usuarios_a_crear.append(usuario)
                usuarios_creados += 1
            else:
                print(f"Las contraseñas no coinciden para el usuario {username}. No se ha creado el usuario.")

        Usuario.objects.bulk_create(usuarios_a_crear)
        print(f"Usuarios cargados con éxito. Total de usuarios creados: {usuarios_creados}")

        return usuarios_creados
    except FileNotFoundError:
        print(f"El archivo JSON no se encuentra en la ruta especificada: {ruta_json}")
        return 0

if __name__ == '__main__':
    ruta_archivo_json = 'login/data/usuarios.json'
    total_usuarios_creados = cargar_usuarios(ruta_archivo_json)

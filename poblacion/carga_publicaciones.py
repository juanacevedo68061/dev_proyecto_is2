import os
import django
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms.settings')
django.setup()

from administracion.models import Categoria
from publicaciones.models import Publicacion_solo_text
from login.models import Usuario

def cargar_publicaciones():
    try:
        ruta_json = 'poblacion/publicaciones.json'

        with open(ruta_json, 'r', encoding='utf-8') as json_file:
            publicaciones_data = json.load(json_file)

        publicaciones_cargadas = 0

        for publicacion_data in publicaciones_data:
            titulo = publicacion_data['titulo']
            autor_nombre = publicacion_data['autor']
            texto = publicacion_data['texto']
            palabras_clave = publicacion_data['palabras_clave']
            categoria_nombre = publicacion_data['categoria']
            estado = publicacion_data['estado']
            likes_usuarios_nombres = publicacion_data.get('likes_usuarios', [])
            dislikes_usuarios_nombres = publicacion_data.get('dislikes_usuarios', [])

            autor = Usuario.objects.get(username=autor_nombre)
            categoria = Categoria.objects.get(nombre=categoria_nombre)

            publicacion = Publicacion_solo_text(
                titulo=titulo,
                autor=autor,
                texto=texto,
                palabras_clave=palabras_clave,
                categoria=categoria,
                estado=estado,
            )
            publicacion.save()
            
            #likes
            usuarios_like = Usuario.objects.filter(username__in=likes_usuarios_nombres)
            publicacion.like_usuario.set(usuarios_like)
            publicacion.likes = usuarios_like.count()

            #dislikes
            usuarios_dislike = Usuario.objects.filter(username__in=dislikes_usuarios_nombres)
            publicacion.dislike_usuario.set(usuarios_dislike)
            publicacion.dislikes = usuarios_dislike.count()

            publicacion.save()

            publicaciones_cargadas += 1
        print(f"Publicaciones cargadas con éxito: {publicaciones_cargadas}")
        return publicaciones_cargadas
    except FileNotFoundError:
        print(f"El archivo JSON no se encuentra en la ruta especificada: {ruta_json}")
        return 0
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")
        return 0

if __name__ == '__main__':
    cargar_publicaciones()

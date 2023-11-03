import os
import django
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms.settings')
django.setup()

from administracion.models import Categoria

def cargar_categorias():
    try:
        ruta_json = 'poblacion/categorias.json'

        with open(ruta_json, 'r', encoding='utf-8') as json_file:
            categorias_data = json.load(json_file)

        categorias_creadas = 0

        for categoria_data in categorias_data:
            nombre = categoria_data['nombre']
            moderada = categoria_data['moderada']
            suscriptores = categoria_data['suscriptores']

            # Crear la categoría
            categoria = Categoria(nombre=nombre, moderada=moderada, suscriptores=suscriptores)
            categoria.save()

            categorias_creadas += 1

        print(f"Categorías creadas con éxito: {categorias_creadas}")
        return categorias_creadas
    except FileNotFoundError:
        print(f"El archivo JSON no se encuentra en la ruta especificada: {ruta_json}")
        return 0
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")
        return 0

if __name__ == '__main__':
    cargar_categorias()

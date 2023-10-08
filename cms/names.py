import importlib
import inspect
from django.apps import apps
from .models import Vistas

def actualizar_nombres_vistas():
    # Obtén todas las aplicaciones en tu proyecto Django
    aplicaciones = apps.get_app_configs()

    for app in aplicaciones:
        try:
            # Importa la views.py de la aplicación actual
            views_module = importlib.import_module(f"{app.name}.views")

            # Obtiene las funciones en views.py que son vistas definidas por el desarrollador
            vistas_desarrollador = [
                nombre for nombre, obj in inspect.getmembers(views_module)
                if inspect.isfunction(obj) and obj.__module__ == views_module.__name__
            ]

            # Almacena los nombres de las vistas como una cadena separada por comas
            nombres_vistas_str = ', '.join(vistas_desarrollador)

            # Actualiza o crea un registro en la tabla Vistas
            Vistas.objects.update_or_create(
                aplicacion=app.name,
                defaults={'vista': nombres_vistas_str}
            )

        except ImportError:
            # Ignora las aplicaciones que no tienen un archivo views.py
            continue

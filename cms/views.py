from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from publicaciones.models import Publicacion  # Importa el modelo de Publicacion

def principal(request):
    """
    Vista para mostrar la página principal con la barra lateral y superior.

    Esta vista muestra una página con la barra lateral y superior, incluyendo opciones para el usuario
    como acceder a su perfil y cerrar sesión.

    Parámetros:
        request: La solicitud HTTP entrante.

    Retorna:
        Renderiza la plantilla principal con la barra lateral y superior.
    """
    # Filtrar las publicaciones con categoría moderada en False
    publicaciones_moderadas = Publicacion.objects.filter(categoria__moderada=False)

    # Puedes pasar la lista de publicaciones a la plantilla para mostrarlas
    contexto = {'publicaciones': publicaciones_moderadas}

    return render(request, 'cms/principal.html', contexto)

    

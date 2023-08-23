from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
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
    return render(request, 'cms/principal.html')

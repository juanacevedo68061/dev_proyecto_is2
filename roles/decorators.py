from functools import wraps
from django.http import HttpResponseForbidden
from .models import Rol

def rol_requerido(rol_nombre):
    """
    Decorador que verifica si el usuario tiene un rol específico antes de permitir el acceso a una vista.

    Parámetros:
        rol_nombre (str): El nombre del rol que se debe verificar.

    Retorna:
        función: La vista decorada.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            """
            Función interna que verifica si el usuario tiene el rol especificado.

            Parámetros:
                request (HttpRequest): La solicitud HTTP.
                *args: Argumentos adicionales.
                **kwargs: Argumentos de palabras clave adicionales.

            Retorna:
                HttpResponse: La respuesta HTTP o un mensaje de "Acceso denegado".
            """
            try:
                # Verifica si el usuario tiene al menos un rol con el nombre especificado
                if request.user.roles.filter(nombre=rol_nombre).exists():
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden("Acceso denegado")
            except Rol.DoesNotExist:
                return HttpResponseForbidden("Acceso denegado")

        return _wrapped_view

    return decorator



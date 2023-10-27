from functools import wraps
from django.urls import reverse
from .models import Rol
from django.shortcuts import render

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
                    return render(request, '403.html', status=403)
            except Rol.DoesNotExist:
                return render(request, '403.html', status=403)

        return _wrapped_view

    return decorator

def permiso_requerido(view_func):
    """
    Decorador que verifica si el usuario tiene un permiso específico en cualquiera de sus roles antes de permitir el acceso a una vista.

    Parámetros:
        view_func: La vista a decorar.

    Retorna:
        función: La vista decorada.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        """
        Función interna que verifica si el usuario tiene el permiso especificado en cualquiera de sus roles.

        Parámetros:
            request (HttpRequest): La solicitud HTTP.
            *args: Argumentos adicionales.
            **kwargs: Argumentos de palabras clave adicionales.

        Retorna:
            HttpResponse: La respuesta HTTP o un mensaje de "Acceso denegado".
        """
        try:
            # Obtener el nombre de la vista
            view_name = view_func.__name__
            
            # Verificar si el usuario tiene el permiso en al menos uno de sus roles
            if any(rol.permisos.filter(codename=view_name).exists() for rol in request.user.roles.all()):
                return view_func(request, *args, **kwargs)
            else:
                return render(request, '403.html', status=403)
        except Rol.DoesNotExist:
            return render(request, '403.html', status=403)

    return _wrapped_view

def permiso_redireccion_requerido(redireccion_url):
    """
    Decorador que verifica si el usuario tiene un permiso específico en cualquiera de sus roles antes de permitir el acceso a una vista.

    Parámetros:
        redireccion_url (str): La URL a la que se redireccionará si el usuario no tiene el permiso.

    Retorna:
        función: La vista decorada.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            """
            Función interna que verifica si el usuario tiene el permiso especificado en cualquiera de sus roles.

            Parámetros:
                request (HttpRequest): La solicitud HTTP.
                *args: Argumentos adicionales.
                **kwargs: Argumentos de palabras clave adicionales.

            Retorna:
                HttpResponse: La respuesta HTTP o una redirección personalizada.
            """
            redireccion= reverse(redireccion_url)
            try:
                # Verificar si el usuario tiene el permiso en al menos uno de sus roles
                if any(rol.permisos.filter(codename=view_func.__name__).exists() for rol in request.user.roles.all()):
                    return view_func(request, *args, **kwargs)
                else:
                    mostrar = "No tienes los permisos necesarios."
                    return render(request, '403.html', {'mostrar':mostrar,'redireccion_url': redireccion}, status=403)
            except Rol.DoesNotExist:
                return render(request, '403.html', status=403)

        return _wrapped_view

    return decorator

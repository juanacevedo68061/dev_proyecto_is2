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

    # Crear una lista de tuplas con la publicación y la imagen del autor si está disponible
    publicaciones_con_imagen = []

    for publicacion in publicaciones_moderadas:
        imagen_autor = None  # Inicializa la variable de imagen como None por defecto
        if publicacion.autor.imagen:
            imagen_autor = publicacion.autor.imagen.url  # Asigna la URL de la imagen si está disponible
        publicaciones_con_imagen.append((publicacion, imagen_autor))

    # Puedes pasar la lista de publicaciones con imagen al contexto
    contexto = {'publicaciones_con_imagen': publicaciones_con_imagen}

    return render(request, 'cms/principal.html', contexto)


    

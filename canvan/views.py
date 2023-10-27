from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from publicaciones.models import Publicacion_solo_text
from roles.decorators import rol_requerido
from django.db.models import Q
from administracion.models import Categoria
from .models import Registro


@login_required
@rol_requerido('autor')
def canvas_autor(request):
    
    """
    Vista para el dashboard de autores. Muestra todas las publicaciones en progreso 
    (borradores y rechazadas) del autor autenticado.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la plantilla 'canvas_autor.html' con las publicaciones en progreso y completadas del autor.
    """
    
    # Obtener todas las publicaciones activas del autor ordenadas por fecha de creación
    en_progreso = Publicacion_solo_text.objects.filter(
    Q(autor=request.user, estado='borrador', activo=True, categoria__moderada=True) |
    Q(autor=request.user, estado='rechazado', para_editor=False, activo=True, categoria__moderada=True)
    )
    completadas = Registro.objects.filter(canvas='autor', usuario=request.user).order_by('fecha_cambio')

    return render(request, 'canvan/canvas_autor.html', {'en_progreso': en_progreso, 'completadas': completadas})

@login_required
@rol_requerido('editor')
def canvas_editor(request):

    """
    Vista para el dashboard de editores. Muestra todas las publicaciones en progreso 
    (en revisión y rechazadas) que requieren la atención de un editor.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la plantilla 'canvas_editor.html' con las publicaciones en progreso y completadas del editor, y todas las categorías.
    """
    
    en_progreso = Publicacion_solo_text.objects.filter(
    Q(estado='revision', activo=True, categoria__moderada=True) |
    Q(estado='rechazado', para_editor=True, activo=True, categoria__moderada=True)
    )

    completadas = Registro.objects.filter(canvas='editor', usuario=request.user).order_by('fecha_cambio')
    categorias = Categoria.objects.all()

    return render(request, 'canvan/canvas_editor.html', {'en_progreso': en_progreso, 'completadas': completadas, 'categorias': categorias})

@login_required
@rol_requerido('publicador')
def canvas_publicador(request):
    
    """
    Vista para el dashboard de publicadores. Muestra todas las publicaciones listas para ser publicadas.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la plantilla 'canvas_publicador.html' con las publicaciones en progreso y completadas del publicador, y todas las categorías.
    """
    
    # Obtener todas las publicaciones activas del publicador ordenadas por fecha de creación
    en_progreso = Publicacion_solo_text.objects.filter(estado='publicar', activo=True, categoria__moderada=True)
    completadas = Registro.objects.filter(canvas='publicador', usuario=request.user).order_by('fecha_cambio')
    categorias = Categoria.objects.all()

    return render(request, 'canvan/canvas_publicador.html', {'en_progreso': en_progreso, 'completadas': completadas, 'categorias': categorias})



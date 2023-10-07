from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from publicaciones.models import Publicacion_solo_text
from roles.decorators import rol_requerido


@login_required
@rol_requerido('autor')
def canvas_autor(request):
    # Obtener todas las publicaciones activas del autor ordenadas por fecha de creación
    en_progreso = Publicacion_solo_text.objects.filter(autor=request.user, estado='borrador', activo=True)
    completadas = Publicacion_solo_text.objects.filter(autor=request.user, estado='revision', activo=True)

    return render(request, 'canvan/canvas_autor.html', {'en_progreso': en_progreso, 'completadas': completadas})

@login_required
@rol_requerido('editor')
def canvas_editor(request):
    en_progreso = Publicacion_solo_text.objects.filter(autor=request.user, estado='revision', activo=True)
    completadas = Publicacion_solo_text.objects.filter(autor=request.user, estado='publicar', activo=True)

    return render(request, 'canvan/canvas_editor.html', {'en_progreso': en_progreso, 'completadas': completadas})

@login_required
@rol_requerido('publicador')
def canvas_publicador(request):
    # Obtener todas las publicaciones activas del publicador ordenadas por fecha de creación
    en_progreso = Publicacion_solo_text.objects.filter(autor=request.user, estado='publicar', activo=True)
    completadas = Publicacion_solo_text.objects.filter(autor=request.user, estado='publicado', activo=True)

    return render(request, 'canvan/canvas_publicador.html', {'en_progreso': en_progreso, 'completadas': completadas})


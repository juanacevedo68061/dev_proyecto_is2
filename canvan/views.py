from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from publicaciones.models import Publicacion_solo_text

@login_required
def canvas_autor(request):
    # Obtener todas las publicaciones del autor ordenadas por fecha de creación
    en_progreso = Publicacion_solo_text.objects.filter(autor=request.user, estado='borrador')
    completadas = Publicacion_solo_text.objects.filter(autor=request.user, estado='revision')

    return render(request, 'canvan/canvas_autor.html', {'en_progreso': en_progreso, 'completadas': completadas})

@login_required
def canvas_editor(request):
    en_progreso = Publicacion_solo_text.objects.filter(autor=request.user, estado='revision')
    completadas = Publicacion_solo_text.objects.filter(autor=request.user, estado='publicar')

    return render(request, 'canvan/canvas_editor.html', {'en_progreso': en_progreso, 'completadas': completadas})

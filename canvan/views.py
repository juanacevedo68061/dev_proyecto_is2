from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from publicaciones.models import Publicacion
from publicaciones.forms import PublicacionForm

def canvas_autor(request):
    # Obtener todas las publicaciones del autor ordenadas por fecha de creación
    publicaciones_borrador = Publicacion.objects.filter(autor=request.user, estado='borrador')
    publicaciones_revision = Publicacion.objects.filter(autor=request.user, estado='revision')

    return render(request, 'canvan/canvas_autor.html', {'publicaciones_borrador': publicaciones_borrador, 'publicaciones_revision': publicaciones_revision})

from django.shortcuts import render
from publicaciones.models import Publicacion_solo_text
from administracion.models import Categoria

def kanban(request):

    publicaciones_borrador = Publicacion_solo_text.objects.filter(estado='borrador', activo=True, categoria__moderada=True)
    publicaciones_revision = Publicacion_solo_text.objects.filter(estado='revision', activo=True, categoria__moderada=True)
    publicaciones_publicar = Publicacion_solo_text.objects.filter(estado='publicar', activo=True, categoria__moderada=True)
    publicaciones_publicado = Publicacion_solo_text.objects.filter(estado='publicado', activo=True, categoria__moderada=True)

    context = {
        'publicaciones_borrador': publicaciones_borrador,
        'publicaciones_revision': publicaciones_revision,
        'publicaciones_publicar': publicaciones_publicar,
        'publicaciones_publicado': publicaciones_publicado,
    }

    return render(request, 'kanban/tablero.html', context)


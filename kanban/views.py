from django.shortcuts import render
from publicaciones.models import Publicacion_solo_text
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from publicaciones.models import Publicacion_solo_text

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

from uuid import UUID
from django.http import Http404

@csrf_exempt
def actualizar(request):
    if request.method == 'POST':
        publicacion_id = request.POST.get('id_publicacion')
        nuevo_estado = request.POST.get('nuevo_estado')
        print(nuevo_estado)
        try:
            publicacion_id = UUID(publicacion_id)
            publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
            
            publicacion.estado = nuevo_estado
            publicacion.save()
            
            return JsonResponse({'message': 'Estado actualizado correctamente'})
        except (ValueError, Http404, Publicacion_solo_text.DoesNotExist) as e:
            return JsonResponse({'error': 'No se encontró la publicación o el ID no es válido'}, status=400)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

from django.shortcuts import render
from publicaciones.models import Publicacion_solo_text
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from publicaciones.models import Publicacion_solo_text
from django.db.models import Q

def kanban(request):

    publicaciones_borrador = Publicacion_solo_text.objects.filter(
    Q(estado='borrador', activo=True, categoria__moderada=True) |
    Q(estado='rechazado', para_editor=False, activo=True, categoria__moderada=True)
    )
    publicaciones_revision = Publicacion_solo_text.objects.filter(
    Q(estado='revision', activo=True, categoria__moderada=True) |
    Q(estado='rechazado', para_editor=True, activo=True, categoria__moderada=True)
    )
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

        estado_valor = {
            "rechazado":0,
            "borrador": 1,
            "revision": 2,
            "publicar": 3,
            "publicado": 4
        }

        if nuevo_estado in estado_valor:
            try:
                publicacion_id = UUID(publicacion_id)
                publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)

                estado_anterior_num = estado_valor[publicacion.estado]
                nuevo_estado_num = estado_valor[nuevo_estado]
                if estado_anterior_num == 0 and publicacion.para_editor:
                    estado_anterior_num=2
                elif estado_anterior_num == 0 and not publicacion.para_editor:
                    estado_anterior_num=1

                publicacion.estado = nuevo_estado
                
                if not(nuevo_estado_num==3 and estado_anterior_num==4) and (estado_anterior_num - nuevo_estado_num) == 1:
                    publicacion.estado = "rechazado"
                    if nuevo_estado_num==2:
                        publicacion.para_editor=True
                    else:
                        publicacion.para_editor=False

                print(publicacion.estado)
                print(publicacion.para_editor)
                publicacion.save()

                return JsonResponse({'message': 'Estado actualizado correctamente'})
            except (ValueError, Http404, Publicacion_solo_text.DoesNotExist) as e:
                return JsonResponse({'error': 'No se encontró la publicación o el ID no es válido'}, status=400)
        else:
            return JsonResponse({'error': 'Estado no válido'}, status=400)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

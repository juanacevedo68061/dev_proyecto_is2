from .forms import CommentForm
from django.http import JsonResponse
from .models import Comment
from django.contrib.auth.decorators import login_required
from publicaciones.models import Publicacion_solo_text
from django.shortcuts import get_object_or_404

@login_required
def comentar(request, publicacion_id):
    """
    Vista para crear un nuevo comentario en una publicación.

    Args:
        request (HttpRequest): El objeto HttpRequest.
        publicacion_id (int): El identificador de la publicación a la que se está comentando.

    Returns:
        JsonResponse: Un objeto JsonResponse que indica si la operación fue exitosa o no.
    """
    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
    response_data = {'success': False}

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.publicacion_id = publicacion_id
            comentario.save()
            publicacion.comments+=1
            publicacion.save()
            print("Comentario: ", comentario)
            
            response_data['success'] = True
    
    return JsonResponse(response_data)

@login_required
def responder(request, comentario_id):
    """
    Vista para responder a un comentario existente.

    Args:
        request (HttpRequest): El objeto HttpRequest.
        comentario_id (int): El identificador del comentario al que se está respondiendo.

    Returns:
        JsonResponse: Un objeto JsonResponse que indica si la operación fue exitosa o no.
    """
    response_data = {'success': False}
    padre = Comment.objects.get(pk=comentario_id)
    
    if request.method == 'POST':
        respuesta_texto = request.POST.get('respuesta_texto')
        form = CommentForm({'texto': respuesta_texto})
        
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.comentario_padre = padre
            comentario.publicacion_id = padre.publicacion_id
            comentario.save()
            publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=padre.publicacion_id)
            publicacion.comments+=1
            publicacion.save()

            response_data['success'] = True
            print("Respuesta: ", comentario)
            print("Padre: ", comentario.comentario_padre)
            
    return JsonResponse(response_data)

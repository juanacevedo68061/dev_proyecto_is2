from .forms import CommentForm
from django.http import JsonResponse
from .models import Comment

def comentar(request, publicacion_id):
    response_data = {'success': False}

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.publicacion_id = publicacion_id
            comentario.save()
            print("Comentario: ", comentario)
            
            response_data['success'] = True
    
    return JsonResponse(response_data)

def responder(request, comentario_id):
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

            response_data['success'] = True
            print("Respuesta: ", comentario)
            print("Padre: ", comentario.comentario_padre)

    return JsonResponse(response_data)
from .forms import CommentForm
from django.http import JsonResponse

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


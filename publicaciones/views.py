import qrcode
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Publicacion
from .forms import PublicacionForm
from .models import Categoria 

@login_required
def crear_publicacion(request):
    categorias = Categoria.objects.all()  # Obtén todas las categorías desde la base de datos

    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.autor = request.user
            
            # Generar código QR
            qr_img = qrcode.make(publicacion.id_publicacion)
            qr_io = BytesIO()
            qr_img.save(qr_io, 'JPEG')
            publicacion.codigo_qr.save('codigo_qr.jpg', ContentFile(qr_io.getvalue()))
            
            # Generar imagen thumbnail
            if publicacion.imagen:
                img = Image.open(publicacion.imagen)
                img.thumbnail((100, 100))
                thumb_io = BytesIO()
                img.save(thumb_io, 'JPEG')
                publicacion.imagen_thumbnail.save('thumbnail.jpg', ContentFile(thumb_io.getvalue()))
            
            publicacion.save()
            return redirect('login:perfil')
    else:
        form = PublicacionForm()
    
    return render(request, 'publicaciones/crear_publicacion.html', {'form': form, 'categorias': categorias})

@login_required
def like_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if request.user not in publicacion.likes.all():
        publicacion.likes.add(request.user)
    return JsonResponse({'likes': publicacion.likes.count()})

@login_required
def dislike_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if request.user not in publicacion.dislikes.all():
        publicacion.dislikes.add(request.user)
    return JsonResponse({'dislikes': publicacion.dislikes.count()})

@login_required
def compartir_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if request.user not in publicacion.share.all():
        publicacion.share.add(request.user)
    return JsonResponse({'compartir': publicacion.share.count()})

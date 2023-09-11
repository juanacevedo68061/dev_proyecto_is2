import qrcode
from io import BytesIO
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Publicacion_solo_text
from .forms import PublicacionForm
from .models import Categoria 
from django.contrib import messages
from django.urls import reverse

@login_required
def crear_publicacion(request):
    categorias = Categoria.objects.all()
    form = PublicacionForm()
    redirect_url = None  # Variable para almacenar la URL de redirección
    message = ''  # Variable para almacenar el mensaje personalizado

    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if 'accion' in request.POST:
            if request.POST['accion'] == 'crear':
                form_fields_required = ['titulo', 'texto', 'categoria', 'palabras_clave']  # Todos los campos requeridos
                message = 'Publicación creada con éxito.'
            elif request.POST['accion'] == 'guardar_borrador':
                form_fields_required = ['titulo']  # Solo el campo "titulo" requerido
                message = 'Borrador guardado con éxito.'

            for field_name, field in form.fields.items():
                field.required = field_name in form_fields_required

            if form.is_valid():
                publicacion = form.save(commit=False)
                publicacion.autor = request.user
                publicacion.estado = 'revision' if request.POST['accion'] == 'crear' else 'borrador'
                publicacion.save()
                messages.success(request, message)
                redirect_url = reverse('canvan:canvas-autor')  # Define la URL de redirección

    return render(request, 'publicaciones/crear_publicacion.html', {'form': form, 'categorias': categorias, 'redirect_url': redirect_url})


@login_required
def editar_publicacion_autor(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion_solo_text, id=publicacion_id)

    if request.method == 'POST':
        form = PublicacionForm(request.POST, instance=publicacion)
        if form.is_valid():
            form.save()
            return redirect('canvan:canvas-autor')

    else:
        form = PublicacionForm(instance=publicacion)

    return render(request, 'publicaciones/editar_publicacion_autor.html', {'form': form, 'publicacion': publicacion})

@login_required
def editar_publicacion_editor(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion_solo_text, id=publicacion_id)

    if request.method == 'POST':
        form = PublicacionForm(request.POST, instance=publicacion)
        if form.is_valid():
            form.save()
            return redirect('canvan:canvas-editor')

    else:
        form = PublicacionForm(instance=publicacion)

    return render(request, 'publicaciones/editar_publicacion_editor.html', {'form': form, 'publicacion': publicacion})

@login_required
def like_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion_solo_text, pk=pk)
    if request.user not in publicacion.likes.all():
        publicacion.likes.add(request.user)
    return JsonResponse({'likes': publicacion.likes.count()})

@login_required
def dislike_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion_solo_text, pk=pk)
    if request.user not in publicacion.dislikes.all():
        publicacion.dislikes.add(request.user)
    return JsonResponse({'dislikes': publicacion.dislikes.count()})

@login_required
def compartir_publicacion(request, pk):
    # Generar código QR
    #qr_img = qrcode.make(publicacion.id_publicacion)
    #qr_io = BytesIO()
    #qr_img.save(qr_io, 'JPEG')
    #publicacion.codigo_qr.save('codigo_qr.jpg', ContentFile(qr_io.getvalue()))
    
    publicacion = get_object_or_404(Publicacion_solo_text, pk=pk)
    if request.user not in publicacion.share.all():
        publicacion.share.add(request.user)
    return JsonResponse({'compartir': publicacion.share.count()})

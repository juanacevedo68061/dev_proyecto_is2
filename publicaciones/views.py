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
    message = ''  # Variable para almacenar el mensaje personalizado
    redirect_url = None  # Variable para almacenar la URL de redirección

    if request.method == 'POST':
        form = PublicacionForm(request.POST, instance=publicacion)
        if 'accion' in request.POST:
            if request.POST['accion'] == 'guardar':
                form_fields_required = ['titulo']
                message = 'Cambios guardados con éxito.'

            elif request.POST['accion'] == 'completar_borrador':
                form_fields_required = ['titulo', 'texto', 'categoria', 'palabras_clave']
                message = 'Borrador completado con éxito.'
            
            for field_name, field in form.fields.items():
                field.required = field_name in form_fields_required

            if form.is_valid():
                publicacion = form.save(commit=False)
                publicacion.estado = 'revision' if request.POST['accion'] == 'completar_borrador' else 'borrador'
                publicacion.save()
                messages.success(request, message)
                redirect_url = reverse('canvan:canvas-autor')  # Define la URL de redirección

    else:
        form = PublicacionForm(instance=publicacion)

    return render(request, 'publicaciones/editar_publicacion_autor.html', {'form': form, 'publicacion': publicacion, 'redirect_url': redirect_url})

@login_required
def eliminar_publicacion_autor(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion_solo_text, id=publicacion_id)
    redirect_url = reverse('canvan:canvas-autor')  # Define la URL de redirección

    if request.method == 'POST':
        # Verifica si se confirma la eliminación
        if 'confirmar_eliminar' in request.POST:
            publicacion.delete()
            messages.success(request, 'La publicación ha sido eliminada con éxito.')

    return render(request, 'publicaciones/eliminar_publicacion_autor.html', {'publicacion': publicacion, 'redirect_url': redirect_url})


@login_required
def editar_publicacion_editor(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion_solo_text, id=publicacion_id)
    message = ''  # Variable para almacenar el mensaje personalizado
    redirect_url = None  # Variable para almacenar la URL de redirección

    if request.method == 'POST':
        form = PublicacionForm(request.POST, instance=publicacion)
        if 'accion' in request.POST:
            if request.POST['accion'] == 'guardar':
                form_fields_required = ['titulo']  # Solo el campo "titulo" requerido
                message = 'Cambios guardados con éxito.'
            elif request.POST['accion'] == 'completar_edicion':
                form_fields_required = ['titulo', 'texto', 'categoria', 'palabras_clave']  # Todos los campos requeridos
                message = 'Edición completada con éxito.'
            
            for field_name, field in form.fields.items():
                field.required = field_name in form_fields_required

            if form.is_valid():
                publicacion = form.save(commit=False)
                publicacion.estado = 'publicar' if request.POST['accion'] == 'completar_edicion' else 'revision'
                publicacion.save()
                messages.success(request, message)
                redirect_url = reverse('canvan:canvas-editor')  
    else:
        form = PublicacionForm(instance=publicacion)

    return render(request, 'publicaciones/editar_publicacion_editor.html', {'form': form, 'publicacion': publicacion, 'redirect_url': redirect_url})

@login_required
def rechazar_editor(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion_solo_text, id=publicacion_id)
    redirect_url = reverse('canvan:canvas-editor')  # Define la URL de redirección

    if request.method == 'POST':
        if 'confirmar_rechazo' in request.POST:
            publicacion.estado = 'borrador'  # Cambiar el estado a "borrador"
            publicacion.save()
            messages.success(request, 'La publicación ha sido rechazada con éxito.')

    return render(request, 'publicaciones/rechazar.html', {'publicacion': publicacion, 'redirect_url': redirect_url})

@login_required
def visualizar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion_solo_text, id=publicacion_id)
    message = ''  # Variable para almacenar el mensaje personalizado
    redirect_url = None  # Variable para almacenar la URL de redirección

    if request.method == 'POST':
        if 'publicar' in request.POST:
            # Cambiar el estado de la publicación a "publicado"
            publicacion.estado = 'publicado'
            publicacion.save()
            message = 'La publicación ha sido publicada con éxito.'
            redirect_url = reverse('canvan:canvas-publicador')
            messages.success(request,message)

    # Filtrar campos que no estén vacíos
    datos_publicacion = {
        'Título': publicacion.titulo,
        'Texto': publicacion.texto,
        'Categoría': publicacion.categoria.nombre,
        'Palabras': publicacion.palabras_clave,
        # Agrega más campos aquí según sea necesario
    }

    # Eliminar campos con valor None o vacío
    datos_publicacion = {campo: valor for campo, valor in datos_publicacion.items() if valor}

    return render(request, 'publicaciones/visualizar_publicacion.html', {'publicacion': publicacion, 'datos_publicacion': datos_publicacion, 'redirect_url': redirect_url})

@login_required
def mostrar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion_solo_text, id=publicacion_id)

    return render(request, 'publicaciones/mostrar_publicacion.html', {'publicacion': publicacion})

@login_required
def rechazar_publicador(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion_solo_text, id=publicacion_id)
    redirect_url = reverse('canvan:canvas-publicador')  # Define la URL de redirección

    if request.method == 'POST':
        if 'confirmar_rechazo' in request.POST:
            publicacion.estado = 'borrador'  # Cambiar el estado a "borrador"
            publicacion.save()
            messages.success(request, 'La publicación ha sido rechazada con éxito.')

    return render(request, 'publicaciones/rechazar.html', {'publicacion': publicacion, 'redirect_url': redirect_url})

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

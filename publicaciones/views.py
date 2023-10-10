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
import uuid
from django.http import HttpResponse
from django.http import JsonResponse

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
                
                # Genera un UUID para la publicación y lo asigna al campo 'id_publicacion'
                publicacion.id_publicacion = uuid.uuid4()
                # Genera la URL absoluta para la publicación
                publicacion.url_publicacion = publicacion.get_absolute_url()

                publicacion.save()
                messages.success(request, message)
                redirect_url = reverse('canvan:canvas-autor')  # Define la URL de redirección

    return render(request, 'publicaciones/crear_publicacion.html', {'form': form, 'categorias': categorias, 'redirect_url': redirect_url})


@login_required
def editar_publicacion_autor(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
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
    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
    redirect_url = reverse('canvan:canvas-autor')  # Define la URL de redirección

    if request.method == 'POST':
        # Verifica si se confirma la eliminación
        if 'confirmar_eliminar' in request.POST:
            publicacion.delete()
            messages.success(request, 'La publicación ha sido eliminada con éxito.')

    return render(request, 'publicaciones/eliminar_publicacion_autor.html', {'publicacion': publicacion, 'redirect_url': redirect_url})


@login_required
def editar_publicacion_editor(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
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
    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
    redirect_url = reverse('canvan:canvas-editor')  # Define la URL de redirección

    if request.method == 'POST':
        if 'confirmar_rechazo' in request.POST:
            publicacion.estado = 'borrador'  # Cambiar el estado a "borrador"
            publicacion.save()
            messages.success(request, 'La publicación ha sido rechazada con éxito.')

    return render(request, 'publicaciones/rechazar.html', {'publicacion': publicacion, 'redirect_url': redirect_url})

@login_required
def mostar_para_publicador(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
    message = ''  # Variable para almacenar el mensaje personalizado
    redirect_url = None  # Variable para almacenar la URL de redirección

    publicador = True  # Establece publicador en True

    if request.method == 'POST':
        if 'publicar' in request.POST:
            # Cambiar el estado de la publicación a "publicado"
            publicacion.estado = 'publicado'
            publicacion.save()
            message = 'La publicación ha sido publicada con éxito.'
            redirect_url = reverse('canvan:canvas-publicador')
            messages.success(request, message)

    return render(
        request,
        'publicaciones/mostar_para_publicador.html',
        {'publicacion': publicacion, 'redirect_url': redirect_url, 'publicador': publicador}
    )


@login_required
def mostrar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)

    return render(request, 'publicaciones/mostrar_publicacion.html', {'publicacion': publicacion})

@login_required
def rechazar_publicador(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
    redirect_url = reverse('canvan:canvas-publicador')  # Define la URL de redirección

    if request.method == 'POST':
        if 'confirmar_rechazo' in request.POST:
            publicacion.estado = 'borrador'  # Cambiar el estado a "borrador"
            publicacion.save()
            messages.success(request, 'La publicación ha sido rechazada con éxito.')

    return render(request, 'publicaciones/rechazar.html', {'publicacion': publicacion, 'redirect_url': redirect_url})

@login_required
def generar_qr(request, publicacion_id):
    # Obtén la publicación con el ID proporcionado
    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)

    # Crea el código QR con la URL de la publicación
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(publicacion.get_absolute_url())  # Utiliza la URL absoluta de la publicación
    qr.make(fit=True)

    # Crea una imagen PIL a partir del código QR
    img = qr.make_image(fill_color="black", back_color="white")

    # Guarda la imagen en un objeto BytesIO
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_data = buffer.getvalue()

    # Devuelve la imagen del código QR como una respuesta HTTP
    response = HttpResponse(content_type="image/png")
    response.write(img_data)
    return response

@login_required
def compartidas(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
    # Incrementa el contador de compartidas
    publicacion.shared += 1
    publicacion.save()
    # Lógica para obtener la cantidad de compartidas para la publicación con publicacion_id
    cantidad_compartidas = publicacion.shared
    # Devuelve la cantidad de compartidas en formato JSON
    data = {'shared_count': cantidad_compartidas}
    return JsonResponse(data)

@login_required
def like(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
    usuario = request.user

    if usuario in publicacion.like_usuario.all():
        # Si el usuario ya le dio "Me gusta", quita el "Me gusta" y decrementa el contador de likes
        publicacion.like_usuario.remove(usuario)
        publicacion.likes -= 1
    else:
        # Si el usuario no le ha dado "Me gusta", agrégale "Me gusta" y aumenta el contador de likes
        publicacion.like_usuario.add(usuario)
        publicacion.likes += 1

    publicacion.save()  # Guarda la publicación actualizada

    return redirect('publicaciones:mostrar_publicacion', publicacion_id=publicacion_id)



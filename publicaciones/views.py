"""
Módulo views.py para gestionar las publicaciones
=============================================
Este módulo contiene las vistas relacionadas con la gestión de publicaciones, 
incluyendo la creación, edición, eliminación, visualización y funcionalidades adicionales 
como generación de códigos QR y gestión de likes/dislikes.
"""


import qrcode
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Publicacion_solo_text
from .forms import PublicacionForm
from django.contrib import messages
from django.urls import reverse
import uuid
from django.http import HttpResponse
from django.http import JsonResponse
from .utils import notificar, publicar_no_moderada
from kanban.models import Registro
from django.utils import timezone
from django.http import HttpResponse
from roles.decorators import permiso_requerido, permiso_redireccion_requerido

@permiso_requerido
@login_required
def crear_publicacion(request):
    """
    Crea una nueva publicación.

    :param request: Objeto HttpRequest.
    :return: Objeto HttpResponse.
    """
    tiene_permiso = publicar_no_moderada(request.user)
    
    form = PublicacionForm(False, tiene_permiso)
    redirect_url = None
    message = ''
    
    if request.method == 'POST':
        form = PublicacionForm(False, tiene_permiso, request.POST, request.FILES)
        if 'accion' in request.POST:
            if request.POST['accion'] == 'crear':
                form_fields_required = ['titulo', 'texto', 'palabras_clave']
                message = 'Publicación creada con éxito.'
            elif request.POST['accion'] == 'guardar_borrador':
                form_fields_required = ['titulo']
                message = 'Borrador creado con éxito.'
                
            for field_name, field in form.fields.items():
                field.required = field_name in form_fields_required

            if form.is_valid():
                publicacion = form.save(commit=False)
                publicacion.autor = request.user
                publicacion.id_publicacion = uuid.uuid4()
                publicacion.url_publicacion = publicacion.get_absolute_url()

                categoria_elegida = None
                categoria_suscriptores = form.cleaned_data.get('categoria_suscriptores')
                categoria_no_suscriptores = form.cleaned_data.get('categoria_no_suscriptores')

                if categoria_suscriptores and not categoria_no_suscriptores:
                    categoria_elegida = categoria_suscriptores
                elif categoria_no_suscriptores and not categoria_suscriptores:
                    categoria_elegida = categoria_no_suscriptores

                publicacion.categoria = categoria_elegida
                if publicacion.categoria:                     
                    if publicacion.categoria.moderada:
                        publicacion.estado = 'revision' if request.POST['accion'] == 'crear' else 'borrador'
                        publicacion.save()                
                        messages.success(request, message)
                        redirect_url = reverse('publicaciones:crear_publicacion')
                    else:                    
                        if request.POST['accion'] == 'crear':
                            publicacion.estado = 'publicado' 
                            publicacion.calcular_vigencia()
                            publicacion.save()                
                            messages.success(request, message)
                            redirect_url = reverse('publicaciones:crear_publicacion')                                            
                        else:
                            message="No esta permitido crear Borradores con Categorias no moderada"
                            messages.error(request, message)
                else:
                    if categoria_suscriptores and categoria_no_suscriptores:
                        message = "Solo se permite seleccionar una categoría."
                    else:
                        message="A falta de Categorias no puedes crear una publicación"
                    messages.error(request, message)

    return render(request, 'publicaciones/crear_publicacion.html', {'form': form, 'redirect_url': redirect_url})

@permiso_redireccion_requerido('kanban:kanban')
@login_required
def editar_publicacion_autor(request, publicacion_id):
    """
    Edita una publicación existente por parte del autor.

    :param request: Objeto HttpRequest.
    :param publicacion_id: ID de la publicación a editar.
    :return: Objeto HttpResponse.
    """

    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
    if request.user != publicacion.autor:
        mostrar = "El acceso es permitido solo al autor de la publicación."
        return render(request, '403.html', {'mostrar':mostrar,'redireccion_url':reverse('kanban:kanban')}, status=403)
    
    message = ''
    redirect_url = None
    if request.method == 'POST':
        form = PublicacionForm(True, False, request.POST, instance=publicacion)
        if 'accion' in request.POST:
            if request.POST['accion'] == 'guardar':
                form_fields_required = ['titulo']
                message = 'Cambios guardados con éxito.'

            elif request.POST['accion'] == 'completar_borrador':
                form_fields_required = ['titulo', 'texto', 'palabras_clave']
                message = 'La publicación ha sido habilitada con éxito.'
            
            for field_name, field in form.fields.items():
                field.required = field_name in form_fields_required

            if form.is_valid():
                publicacion = form.save(commit=False)
                
                categoria_elegida = None
                categoria_suscriptores = form.cleaned_data.get('categoria_suscriptores')
                categoria_no_suscriptores = form.cleaned_data.get('categoria_no_suscriptores')

                if categoria_suscriptores and not categoria_no_suscriptores:
                    categoria_elegida = categoria_suscriptores
                elif categoria_no_suscriptores and not categoria_suscriptores:
                    categoria_elegida = categoria_no_suscriptores

                publicacion.categoria = categoria_elegida
                if publicacion.categoria:
                    if request.POST['accion'] == 'completar_borrador':
                        publicacion.semaforo = "verde" 
                    else:
                        publicacion.semaforo = "amarillo"            
                    publicacion.save()
                    messages.success(request, message)
                    redirect_url = reverse('kanban:kanban')
                else:
                    if categoria_suscriptores and categoria_no_suscriptores:
                        message = "Solo se permite seleccionar una categoría."
                    elif not categoria_suscriptores and not categoria_no_suscriptores:
                        message="A falta de Categorias no puedes crear una publicación"
                    messages.error(request, message)
    else:
        form = PublicacionForm(instance=publicacion)

    return render(request, 'publicaciones/editar_publicacion_autor.html', {'form': form, 'publicacion': publicacion, 'redirect_url': redirect_url})

@permiso_redireccion_requerido('kanban:kanban')
@login_required
def editar_publicacion_editor(request, publicacion_id):

    """
    Edita una publicación existente por parte del editor.

    :param request: Objeto HttpRequest.
    :param publicacion_id: ID de la publicación a editar.
    :return: Objeto HttpResponse.
    """

    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
    message = ''  # Variable para almacenar el mensaje personalizado
    redirect_url = None  # Variable para almacenar la URL de redirección

    if request.method == 'POST':
        form = PublicacionForm(True, False, request.POST, instance=publicacion)
        if 'accion' in request.POST:
            if request.POST['accion'] == 'guardar':
                form_fields_required = ['titulo']  # Solo el campo "titulo" requerido
                message = 'Cambios guardados con éxito.'
            elif request.POST['accion'] == 'completar_edicion':
                form_fields_required = ['titulo', 'texto', 'categoria', 'palabras_clave']  # Todos los campos requeridos
                message = 'La publicación ha sido habilitada con éxito.'
            
            for field_name, field in form.fields.items():
                field.required = field_name in form_fields_required

            if form.is_valid():
                publicacion = form.save(commit=False)
                
                categoria_elegida = None
                categoria_suscriptores = form.cleaned_data.get('categoria_suscriptores')
                categoria_no_suscriptores = form.cleaned_data.get('categoria_no_suscriptores')

                if categoria_suscriptores and not categoria_no_suscriptores:
                    categoria_elegida = categoria_suscriptores
                elif categoria_no_suscriptores and not categoria_suscriptores:
                    categoria_elegida = categoria_no_suscriptores

                publicacion.categoria = categoria_elegida
                if publicacion.categoria:
                    if request.POST['accion'] == 'completar_edicion':
                        publicacion.semaforo = "verde" 
                    else:
                        publicacion.semaforo = "amarillo"            
                    
                    publicacion.save()
                    messages.success(request, message)
                    redirect_url = reverse('kanban:kanban')  
                else:
                    if categoria_suscriptores and categoria_no_suscriptores:
                        message = "Solo se permite seleccionar una categoría."
                    elif not categoria_suscriptores and not categoria_no_suscriptores:
                        message="A falta de Categorias no puedes crear una publicación"
                    messages.error(request, message)
    else:
        form = PublicacionForm(instance=publicacion)

    return render(request, 'publicaciones/editar_publicacion_editor.html', {'form': form, 'publicacion': publicacion, 'redirect_url': redirect_url})

@permiso_redireccion_requerido('kanban:kanban')
@login_required
def mostar_para_publicador(request, publicacion_id):

    """
    Muestra una publicación para el publicador.

    :param request: Objeto HttpRequest.
    :param publicacion_id: ID de la publicación a mostrar.
    :return: Objeto HttpResponse.
    """

    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
    message = ''  # Variable para almacenar el mensaje personalizado
    redirect_url = None  # Variable para almacenar la URL de redirección

    publicador = True  # Establece publicador en True

    if request.method == 'POST':
        if 'publicar' in request.POST:
            # Cambiar el estado de la publicación a "publicado"
            publicacion.semaforo = "verde"
            publicacion.fecha_publicacion = timezone.now().date()
            publicacion.save()
            
            message = 'La publicación ha sido habilitada con éxito.'
            redirect_url = reverse('kanban:kanban')
            messages.success(request, message)

    return render(
        request,
        'publicaciones/mostar_para_publicador.html',
        {'publicacion': publicacion, 'redirect_url': redirect_url, 'publicador': publicador}
    )

def mostrar_publicacion(request, publicacion_id):

    """
    Muestra una publicación al usuario.

    :param request: Objeto HttpRequest.
    :param publicacion_id: ID de la publicación a mostrar.
    :return: Objeto HttpResponse.
    """

    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
    ha_dado_like = publicacion.like_usuario.filter(id=request.user.id).exists()
    ha_dado_dislike = publicacion.dislike_usuario.filter(id=request.user.id).exists()
    
    rol_publicador = None
    if request.user.is_authenticated:
        if request.user.roles.filter(nombre="publicador").exists():
            rol_publicador = True
    context = {
        'publicacion': publicacion,
        'ha_dado_like': ha_dado_like,
        'ha_dado_dislike': ha_dado_dislike,
        'rol_publicador': rol_publicador
    }

    return render(request, 'publicaciones/mostrar_publicacion.html', context)

def generar_qr(request, publicacion_id):

    """
    Genera un código QR que redirige a una publicación.

    :param request: Objeto HttpRequest.
    :param publicacion_id: ID de la publicación para la que se genera el QR.
    :return: Objeto HttpResponse con la imagen del código QR.
    """

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

def compartidas(request, publicacion_id):

    """
    Gestiona el contador de veces que una publicación ha sido compartida.

    :param request: Objeto HttpRequest.
    :param publicacion_id: ID de la publicación compartida.
    :return: Objeto JsonResponse con la cantidad de veces compartida.
    """

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

    """
    Gestiona los likes de una publicación.

    :param request: Objeto HttpRequest.
    :param publicacion_id: ID de la publicación que recibe el like.
    :return: Objeto JsonResponse con la cantidad de likes y el estado del like del usuario.
    """

    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
    usuario = request.user
    tiene_dislike = False
    if usuario in publicacion.dislike_usuario.all():
        # Si el usuario ya le dio "No me gusta", quita el "No me gusta" y decrementa el contador de dislikes
        publicacion.dislike_usuario.remove(usuario)
        publicacion.dislikes -= 1
        tiene_dislike = True
    if usuario in publicacion.like_usuario.all():
        # Si el usuario ya le dio "Me gusta", quita el "Me gusta" y decrementa el contador de likes
        publicacion.like_usuario.remove(usuario)
        publicacion.likes -= 1
        ha_dado_like = False
    else:
        # Si el usuario no le ha dado "Me gusta", agrégale "Me gusta" y aumenta el contador de likes
        publicacion.like_usuario.add(usuario)
        publicacion.likes += 1
        ha_dado_like = True

    publicacion.save()  # Guarda la publicación actualizada

    # Devuelve una respuesta JSON con la nueva cantidad de likes y si el usuario dio "Me gusta"
    response_data = {
        'likes': publicacion.likes,
        'dislikes': publicacion.dislikes,
        'ha_dado_like': ha_dado_like,
        'tiene_dislike': tiene_dislike,
    }

    return JsonResponse(response_data)

@login_required
def dislike(request, publicacion_id):

    """
    Gestiona los dislikes de una publicación.

    :param request: Objeto HttpRequest.
    :param publicacion_id: ID de la publicación que recibe el dislike.
    :return: Objeto JsonResponse con la cantidad de dislikes y el estado del dislike del usuario.
    """

    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
    usuario = request.user
    tiene_like = False

    if usuario in publicacion.like_usuario.all():
        # Si el usuario ya le dio "Me gusta", quita el "Me gusta" y decrementa el contador de likes
        publicacion.like_usuario.remove(usuario)
        publicacion.likes -= 1
        tiene_like = True

    if usuario in publicacion.dislike_usuario.all():
        # Si el usuario ya le dio "No me gusta", quita el "No me gusta" y decrementa el contador de dislikes
        publicacion.dislike_usuario.remove(usuario)
        publicacion.dislikes -= 1
        ha_dado_dislike = False
    else:
        # Si el usuario no le ha dado "No me gusta", agrégale "No me gusta" y aumenta el contador de dislikes
        publicacion.dislike_usuario.add(usuario)
        publicacion.dislikes += 1
        ha_dado_dislike = True

    publicacion.save()  # Guarda la publicación actualizada

    # Devuelve una respuesta JSON con la nueva cantidad de likes, dislikes y las respectivas banderas
    response_data = {
        'likes': publicacion.likes,
        'dislikes': publicacion.dislikes,
        'ha_dado_dislike': ha_dado_dislike,
        'tiene_like': tiene_like,
    }

    return JsonResponse(response_data)

def track_view(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
    publicacion.views += 1
    publicacion.save()
    return JsonResponse({'status': 'success', 'views': publicacion.views})

@login_required
def estado(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
    publicacion.activo = not publicacion.activo
    publicacion.save()
    if(not publicacion.activo):
        notificar(publicacion,1)
        registros_a_eliminar = Registro.objects.filter(usuario=request.user, publicacion_id=publicacion_id)
        registros_a_eliminar.delete()
    return JsonResponse({'activo': publicacion.activo})

@login_required
def registrar(request, publicacion, kanban):
    nuevo_registro = Registro.objects.create(
        usuario=request.user,
        publicacion_id=publicacion.id_publicacion,
        publicacion_titulo=publicacion.titulo,
        nuevo_estado=publicacion.estado,
        kanban = kanban
    )
    nuevo_registro.save()

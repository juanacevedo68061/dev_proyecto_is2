"""
Módulo views.py para gestionar las publicaciones
================================================
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
from .models import Publicacion_solo_text, Calificacion
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
import json
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_comments_xtd.models import XtdComment
from django_comments.views.comments import post_comment

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
    """
    Incrementa el contador de vistas de una publicación y devuelve el número actualizado de vistas.

    Args:
        request: Objeto HttpRequest.
        publicacion_id: ID de la publicación que se está viendo.

    Returns:
        JsonResponse con el estado y el número de vistas actualizado.
    """
    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
    publicacion.views += 1
    publicacion.save()
    return JsonResponse({'status': 'success', 'views': publicacion.views})

@login_required
def estado(request, publicacion_id):
    """
    Cambia el estado activo/inactivo de una publicación. 
    Si la publicación se desactiva, notifica y elimina los registros asociados.

    Args:
        request: Objeto HttpRequest.
        publicacion_id: ID de la publicación cuyo estado se está cambiando.

    Returns:
        JsonResponse con el estado activo/inactivo actualizado.
    """
    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
    publicacion.activo = not publicacion.activo
    publicacion.save()
    if(not publicacion.activo):
        notificar(publicacion,1)
        registros_a_eliminar = Registro.objects.filter(responsable=request.user, publicacion_id=publicacion_id)
        registros_a_eliminar.delete()
    return JsonResponse({'activo': publicacion.activo})

@login_required
def estatus(request, publicacion_id):
    """
    Cambia el estatus de una publicación. 

    Args:
        request: Objeto HttpRequest.
        publicacion_id: ID de la publicación cuyo estado se está cambiando.

    Returns:
        JsonResponse con el estatus.
    """
    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
    publicacion.destacado = not publicacion.destacado
    publicacion.save()
    return JsonResponse({'destacado': publicacion.destacado})

@login_required
@require_http_methods(["GET", "POST"])
def calificar(request, publicacion_id):
    """
    Permite a un usuario calificar o modificar su calificación para una publicación. 
    Si es un POST, establece o actualiza la calificación. 
    Si es un GET, recupera la calificación actual del usuario.

    Args:
        request: Objeto HttpRequest.
        publicacion_id: ID de la publicación que se está calificando.

    Returns:
        JsonResponse con la calificación y el total de calificaciones. 
        Si el método HTTP no está permitido, devuelve un HttpResponseBadRequest.
    """
    publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
    usuario = request.user
    if request.method == "POST":
        data = json.loads(request.body)
        rating = data.get('rating')
        publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)

        try:
            calificacion = publicacion.calificaciones.get(usuario=usuario)
            if rating == calificacion.rating:
                publicacion.calificaciones.remove(calificacion)
                calificacion.delete()
                publicacion.calificaciones_cantidad -= 1
                publicacion.save()
                rating = 0
            else:
                calificacion.rating = rating
                calificacion.save()
        except Calificacion.DoesNotExist:
            calificacion = Calificacion(usuario=usuario, rating=rating)
            calificacion.save()
            publicacion.calificaciones.add(calificacion)
            publicacion.calificaciones_cantidad += 1
            publicacion.save()

        cantidad = publicacion.calificaciones_cantidad
        return JsonResponse({'rating': rating, 'calificaciones': cantidad})

    if request.method == "GET":
        try:
            calificacion = publicacion.calificaciones.get(usuario=usuario)
            rating = calificacion.rating
        except Calificacion.DoesNotExist:
            rating = 0

        cantidad = publicacion.calificaciones_cantidad

        return JsonResponse({'rating': rating, 'calificaciones': cantidad})

    return HttpResponseBadRequest('Método no permitido')

@receiver(post_save, sender=XtdComment)
def update_comment_count(sender, instance, created, **kwargs):
    """
    Actualiza el contador de comentarios de un objeto relacionado cuando se crea un nuevo comentario.

    Args:
        sender: Modelo que envía la señal.
        instance: Instancia del comentario que fue guardado.
        created: Booleano que indica si la instancia fue creada.
    """
    if created:
        instance.content_object.comments += 1
        instance.content_object.save()

@receiver(post_delete, sender=XtdComment)
def decrease_comment_count(sender, instance, **kwargs):
    """
    Actualiza el contador de comentarios de un objeto relacionado cuando se elimina un comentario.

    Args:
        sender: Modelo que envía la señal.
        instance: Instancia del comentario que fue eliminado.
    """
    instance.content_object.comments -= 1
    instance.content_object.save()

@login_required
def custom_post_comment(request):
    """
    Procesa y envía un comentario. Si el comentario se envía correctamente, 
    devuelve una respuesta JSON indicando el éxito, de lo contrario, indica un error.

    Args:
        request: Objeto HttpRequest.

    Returns:
        JsonResponse indicando el estado y el mensaje relacionado con el envío del comentario.
    """
    response = post_comment(request)
    
    # Si el comentario se creó correctamente, devuelve una respuesta JSON.
    if response.status_code == 302:
        return JsonResponse({"status": "success", "message": "Comentario enviado con éxito!"})
    else:
        return JsonResponse({"status": "error", "message": "Hubo un error al enviar el comentario."})
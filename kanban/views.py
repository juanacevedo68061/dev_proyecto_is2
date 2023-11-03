from django.shortcuts import render
from publicaciones.models import Publicacion_solo_text
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from publicaciones.models import Publicacion_solo_text
from django.db.models import Q
from uuid import UUID
from django.http import Http404
from publicaciones.utils import tiene_rol
from roles.decorators import permiso_requerido
from django.contrib.auth.decorators import login_required
from .models import Registro
from administracion.models import Categoria
from publicaciones.utils import notificar
from login.models import Usuario

@permiso_requerido
@login_required
def kanban(request):
    """
    Vista para mostrar el tablero Kanban de la aplicación.

    Esta vista muestra las publicaciones en diferentes columnas según su estado.

    Parameters:
    -----------
    request : HttpRequest
        La solicitud HTTP recibida.

    Returns:
    --------
    HttpResponse
        Una respuesta HTTP que renderiza el tablero Kanban.
    """
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

    categorias = Categoria.objects.filter(moderada=True)
    context = {
        'publicaciones_borrador': publicaciones_borrador,
        'publicaciones_revision': publicaciones_revision,
        'publicaciones_publicar': publicaciones_publicar,
        'publicaciones_publicado': publicaciones_publicado,
        'categorias': categorias
    }

    return render(request, 'kanban/tablero.html', context)

@permiso_requerido
@login_required
@csrf_exempt
def actualizar(request):
    """
    Vista para actualizar el estado de una publicación en el tablero Kanban.

    Permite cambiar el estado de una publicación y realiza validaciones de permisos.

    Parameters:
    -----------
    request : HttpRequest
        La solicitud HTTP recibida.

    Returns:
    --------
    JsonResponse
        Una respuesta JSON con el resultado de la actualización.
    """

    if request.method == 'POST':
        publicacion_id = request.POST.get('id_publicacion')        
        nuevo_estado = request.POST.get('nuevo_estado')

        estado_valor = {
            "rechazado": 0,
            "borrador": 1,
            "revision": 2,
            "publicar": 3,
            "publicado": 4
        }

        if nuevo_estado in estado_valor:
            try:
                publicacion_id = UUID(publicacion_id)
                publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
                anterior = publicacion.estado
                nuevo = nuevo_estado
                publicacion.estado = nuevo
                
                #asignacion temporal si estan rechazados
                if anterior == "rechazado" and publicacion.para_editor:
                    anterior="revision"
                elif anterior == "rechazado" and not publicacion.para_editor:
                    anterior = "borrador"
                
                #No se permiten recambios de estado en la misma columna
                if anterior == "borrador" and nuevo == "borrador":
                    return JsonResponse({'vuelve': True})
                if anterior == "revision" and nuevo == "revision":
                    return JsonResponse({'vuelve': True})
                if anterior == "publicar" and nuevo == "publicar":
                    return JsonResponse({'vuelve': True})
                if anterior == "publicado" and nuevo == "publicado":
                    return JsonResponse({'vuelve': True})
                                                
                #esta accion se restringe para el que no es el autor
                if nuevo == "revision" and anterior == "borrador" and not request.user == publicacion.autor:
                    return JsonResponse({'autor': True})
                
                #acciones no permitidas
                #publicado a revision
                #publicado a borrador
                #borrador a publicar
                #borrador a publicado
                #revision a publicado
                if anterior == "publicado" and nuevo == "revision":
                    return JsonResponse({'accion': False})
                if anterior == "publicado" and nuevo == "borrador":
                    return JsonResponse({'accion': False})
                if anterior == "borrador" and nuevo == "publicar":
                    return JsonResponse({'accion': False})
                if anterior == "borrador" and nuevo == "publicado":
                    return JsonResponse({'accion': False})
                if anterior == "revision" and nuevo == "publicado":
                    return JsonResponse({'accion': False})

                #Estas acciones corresponden a rechazos
                if nuevo == "borrador" and anterior == "revision" and tiene_rol(request.user, "editor"):
                    return JsonResponse({'reason_required': True})
                elif nuevo == "borrador" and anterior == "revision" and not tiene_rol(request.user, "editor"):
                    return JsonResponse({'rol': "editor"})
                if nuevo == "revision" and anterior == "publicar" and tiene_rol(request.user, "publicador"):
                    return JsonResponse({'reason_required': True})
                elif nuevo == "revision" and anterior == "publicar" and not tiene_rol(request.user, "publicador"):
                    return JsonResponse({'rol': "publicador"})
                if nuevo == "borrador" and anterior == "publicar" and tiene_rol(request.user, "publicador"):
                    return JsonResponse({'reason_required': True})
                elif nuevo == "borrador" and anterior == "publicar" and not tiene_rol(request.user, "publicador"):
                    return JsonResponse({'rol': "publicador"})
                
                #acciones que corresponden a ciertos roles
                if nuevo == "publicar" and anterior == "revision" and not tiene_rol(request.user, "editor"):
                    return JsonResponse({'rol': "editor"})
                if nuevo == "publicado" and anterior == "publicar" and not tiene_rol(request.user, "publicador"):
                    return JsonResponse({'rol': "publicador"})
                if nuevo == "publicar" and anterior == "publicado" and not tiene_rol(request.user, "publicador"):
                    return JsonResponse({'rol': "publicador"})
                
                print(publicacion.estado)
                print(publicacion.para_editor)
                print(publicacion.semaforo)
                
                publicacion.semaforo = "rojo"                
                if publicacion.estado == "publicado":
                    publicacion.semaforo = "verde"

                publicacion.save()
                if not publicacion.estado == "borrador":
                    notificar(publicacion,3)

                registrar(request, publicacion, anterior)
                
                return JsonResponse({'vuelve': True})
            except (ValueError, Http404, Publicacion_solo_text.DoesNotExist) as e:
                return JsonResponse({'error': 'No se encontró la publicación o el ID no es válido'}, status=400)
        else:
            return JsonResponse({'error': 'Estado no válido'}, status=400)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

@permiso_requerido
@login_required
@csrf_exempt
def motivo(request):
    """
    Vista para proporcionar un motivo al rechazar una publicación en el tablero Kanban.

    Permite agregar un motivo al rechazar una publicación y cambia su estado.

    Parameters:
    -----------
    request : HttpRequest
        La solicitud HTTP recibida.

    Returns:
    --------
    JsonResponse
        Una respuesta JSON con el resultado de la operación.
    """
    if request.method == 'POST':
        publicacion_id = request.POST.get('id_publicacion')
        publicacion_id = UUID(publicacion_id)
        publicacion = get_object_or_404(Publicacion_solo_text, id_publicacion=publicacion_id)
        motivo = request.POST.get('motivo')
        nuevo = request.POST.get('nuevo')
        if motivo:
            print(motivo)
            
            if nuevo == "revision":
                publicacion.para_editor = True
                motivo = motivo + ", su publicación se pasó al Editor"
            elif nuevo == "borrador":
                publicacion.para_editor = False
            anterior = publicacion.estado
            publicacion.estado ="rechazado"
            publicacion.semaforo = "rojo"
            publicacion.save()          
            notificar(publicacion,2, motivo) 
            registrar(request, publicacion, anterior) 
            print(publicacion.estado)
            print(publicacion.para_editor)
            
            return JsonResponse({'vuelve': True})
        else:
            print("VACIOOOOO")
            return JsonResponse({'vuelve': True})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
@login_required
def historial(request, publicacion_id):
    """
    Vista para ver el historial de cambios de una publicación en el tablero Kanban.

    Permite ver el historial de registros de cambios de una publicación específica.

    Parameters:
    -----------
    request : HttpRequest
        La solicitud HTTP recibida.
    publicacion_id : UUID
        El ID único de la publicación.

    Returns:
    --------
    HttpResponse
        Una respuesta HTTP que renderiza el historial de cambios de la publicación.
    """
    registros = Registro.objects.filter(publicacion_id=publicacion_id)
    if not tiene_rol(request.user, "editor") and not tiene_rol(request.user, "publicador"):
        registros = Registro.objects.filter(publicacion_id=publicacion_id, responsable=request.user)
    return render(request, 'kanban/historial.html', {'registros': registros})

@login_required
def registrar(request, publicacion, anterior):
    """
    Función para registrar un cambio de estado en el historial de una publicación.

    Registra un nuevo registro de cambio en el historial de la publicación.

    Parameters:
    -----------
    request : HttpRequest
        La solicitud HTTP recibida.
    publicacion : Publicacion_solo_text
        La instancia de la publicación.
    anterior : str
        El estado anterior de la publicación.

    Returns:
    --------
    None
    """
    usuario = request.user
    roles = usuario.roles.all()
    nuevo_registro = Registro.objects.create(
        responsable=usuario,
        publicacion_id=publicacion.id_publicacion,
        publicacion_titulo=publicacion.titulo,
        anterior = anterior,
        nuevo=publicacion.estado,
    )
    nuevo_registro.roles.set(roles)
    nuevo_registro.save()
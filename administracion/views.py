from django.shortcuts import render, get_object_or_404
from .models import Categoria
from .forms import CategoriaForm, AsignarPermisosForm, EliminarPermisosForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from roles.decorators import rol_requerido, permiso_requerido
from roles.models import Rol
from login.models import Usuario
from django.urls import reverse
from roles.forms import AgregarRolForm

@rol_requerido('administrador')
@login_required
def panel(request):
    """
    Vista para el panel de administración.

    Parámetros:
        request (HttpRequest): La solicitud HTTP entrante.

    Retorna:
        HttpResponse: Redirecciona a la vista del panel de administración principal.
    """
    # Tu lógica para el panel principal va aquí
    return render(request, 'administracion/panel.html')

@rol_requerido('administrador')
@permiso_requerido
@login_required
def gestion_categorias(request):
    """
    Vista para listar categorías.

    Parámetros:
        request (HttpRequest): La solicitud HTTP entrante.

    Retorna:
        HttpResponse: Muestra la lista de categorías.
    """
    categorias = Categoria.objects.all()
    return render(request, 'administracion/gestion_categorias.html', {'categorias': categorias})

@rol_requerido('administrador')
@permiso_requerido
@login_required
def crear_categoria(request):
    """
    Vista para crear una nueva categoría.

    Parámetros:
        request (HttpRequest): La solicitud HTTP entrante.

    Retorna:
        HttpResponse: Redirecciona a la vista de lista de categorías si la categoría se crea con éxito,
        o muestra el formulario de creación de categoría con errores.
    """
    redirect_url = None
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'La categoría se ha creado correctamente.')
            redirect_url = reverse('administracion:gestion_categorias')
        else:
            messages.error(request, 'Hubo un problema al crear la categoría. Por favor, verifica los datos ingresados.')
            redirect_url = request.path
    else:
        form = CategoriaForm()

    return render(request, 'administracion/crear_categoria.html', {'form': form,'redirect_url': redirect_url})

@rol_requerido('administrador')
@permiso_requerido
@login_required
def editar_categoria(request, categoria_id):
    """
    Vista para editar una categoría existente.

    Parámetros:
        request (HttpRequest): La solicitud HTTP entrante.
        categoria_id (int): El ID de la categoría que se va a editar.

    Retorna:
        HttpResponse: Redirecciona a la vista de lista de categorías si la categoría se edita con éxito,
        o muestra el formulario de edición de categoría con errores.
    """
    redirect_url = None
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'La categoría se ha actualizado correctamente.')
            redirect_url = reverse('administracion:gestion_categorias')
        else:
            messages.error(request, 'Hubo un problema al actualizar la categoría. Por favor, verifica los datos ingresados.')
            redirect_url = request.path
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'administracion/editar_categoria.html', {'form': form, 'categoria': categoria, 'redirect_url': redirect_url})

@rol_requerido('administrador')
@permiso_requerido
@login_required
def eliminar_categoria(request, categoria_id):
    """
    Vista para eliminar una categoría existente.

    Parámetros:
        request (HttpRequest): La solicitud HTTP entrante.
        categoria_id (int): El ID de la categoría que se va a eliminar.

    Retorna:
        HttpResponse: Redirecciona a la vista de lista de categorías si la categoría se elimina con éxito,
        o muestra la confirmación de eliminación de categoría con errores.
    """
    redirect_url = None
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'La categoría se ha eliminado correctamente.')
        redirect_url = reverse('administracion:gestion_categorias')
    return render(request, 'administracion/eliminar_categoria.html', {'categoria': categoria, 'redirect_url': redirect_url})

@rol_requerido('administrador')
@permiso_requerido
@login_required
def gestion_usuarios(request):
    """
    Vista para gestionar usuarios.

    Parámetros:
        request (HttpRequest): La solicitud HTTP entrante.

    Retorna:
        HttpResponse: Muestra la lista de usuarios y opciones de eliminación.
    """
    usuarios = Usuario.objects.all()
    return render(request, 'administracion/gestion_usuarios.html', {'usuarios': usuarios})

@rol_requerido('administrador')
@permiso_requerido
@login_required
def eliminar_usuario(request, usuario_id):
    """
    Vista para eliminar un usuario existente.

    Esta vista permite a un administrador eliminar un usuario existente del sistema.
    
    Parámetros:
        request (HttpRequest): La solicitud HTTP entrante.
        usuario_id (int): El ID del usuario que se va a eliminar.

    Retorna:
        HttpResponse: Una respuesta HTTP que redirige al administrador a la lista de usuarios
                      después de eliminar el usuario especificado.

    """
    usuario = get_object_or_404(Usuario, id=usuario_id)
    redirect_url = None
    if request.method == 'POST':
        if usuario == request.user:    
            messages.error(request, 'No puedes eliminarte a ti mismo.')
        else:
            usuario.delete()
            messages.success(request, 'Usuario eliminado correctamente.')
        redirect_url = reverse('administracion:gestion_usuarios')

    return render(request, 'administracion/eliminar_usuario.html', {'usuario': usuario, 'redirect_url': redirect_url})

@rol_requerido('administrador')
@permiso_requerido
@login_required
def asignar_roles_usuario(request, usuario_id):
    """
    Vista para asignar roles a un usuario existente.

    Esta vista permite a un administrador asignar roles a un usuario existente en el sistema.

    Parámetros:
        request (HttpRequest): La solicitud HTTP entrante.
        usuario_id (int): El ID del usuario al que se le asignarán roles.

    Retorna:
        HttpResponse: Una respuesta HTTP que redirige al administrador a la gestión de usuarios
                      después de asignar los roles al usuario especificado.

    """    
    usuario = get_object_or_404(Usuario, id=usuario_id)
    redirect_url = None
    # Obtener los nombres de roles que el usuario aún no tiene asignados
    roles_asignados_nombres = usuario.roles.values_list('nombre', flat=True)
    roles_disponibles = [rol[0] for rol in Rol.ROLES if rol[0] not in roles_asignados_nombres]

    if request.method == 'POST':
        roles_seleccionados = request.POST.getlist('roles')
        for rol_nombre in roles_seleccionados:
            # Crear una nueva instancia del rol y asignarlo al usuario
            if rol_nombre not in roles_asignados_nombres:
                Rol.objects.create(nombre=rol_nombre)
                usuario.roles.create(nombre=rol_nombre)
        messages.success(request, 'Roles asignados correctamente.')
        redirect_url = reverse('administracion:gestion_usuarios')

    return render(request, 'administracion/asignar_roles_usuario.html', {'usuario': usuario, 'roles_disponibles': roles_disponibles, 'redirect_url': redirect_url})

@rol_requerido('administrador')
@permiso_requerido
@login_required
def eliminar_roles_usuario(request, usuario_id):
    """
    Vista para eliminar roles de un usuario existente.

    Esta vista permite a un administrador eliminar roles de un usuario existente en el sistema.

    Parámetros:
        request (HttpRequest): La solicitud HTTP entrante.
        usuario_id (int): El ID del usuario del que se eliminarán roles.

    Retorna:
        HttpResponse: Una respuesta HTTP que redirige al administrador a la gestión de usuarios
                      después de eliminar los roles del usuario especificado.

    """
    usuario = get_object_or_404(Usuario, id=usuario_id)
    redirect_url = None
    if request.method == 'POST':
        roles_seleccionados = request.POST.getlist('roles')
        for rol_id in roles_seleccionados:
            rol = Rol.objects.get(id=rol_id)
            usuario.roles.remove(rol)
        messages.success(request, 'Roles eliminados correctamente.')
        redirect_url = reverse('administracion:gestion_usuarios')

    roles_asignados = usuario.roles.all()
    return render(request, 'administracion/eliminar_roles_usuario.html', {'usuario': usuario, 'roles_asignados': roles_asignados, 'redirect_url': redirect_url})

@rol_requerido('administrador')
@permiso_requerido
@login_required
def agregar_permisos_roles_usuario(request, usuario_id):
    """
    Vista para agregar permisos a los roles de un usuario existente.

    Esta vista permite a un administrador agregar permisos a los roles de un usuario existente en el sistema.

    Parámetros:
        request (HttpRequest): La solicitud HTTP entrante.
        usuario_id (int): El ID del usuario al que se le asignarán permisos a sus roles.

    Retorna:
        HttpResponse: Una respuesta HTTP que redirige al administrador a la gestión de usuarios
                      después de agregar los permisos a los roles del usuario especificado.

    """    
    redirect_url = None
    usuario = Usuario.objects.get(id=usuario_id)
    roles_asignados = usuario.roles.all()

    if request.method == 'POST':
        form = AsignarPermisosForm(request.POST, roles_asignados=roles_asignados)
        if form.is_valid():
            rol_id = form.cleaned_data['rol'].id
            permisos_seleccionados = form.cleaned_data['permisos']

            # Obtener el rol seleccionado
            rol = Rol.objects.get(id=rol_id)

            # Crear permisos y asignarlos al rol
            for permiso_nombre in permisos_seleccionados:
                permiso, _ = Permission.objects.get_or_create(
                    codename=permiso_nombre,
                    content_type=ContentType.objects.get_for_model(Rol),
                    defaults={'name': f'Permiso {permiso_nombre}'}
                )
                rol.permisos.add(permiso)
            messages.success(request, 'Permisos agregados correctamente.')
            redirect_url = reverse('administracion:gestion_usuarios')
    else:
        form = AsignarPermisosForm(roles_asignados=roles_asignados)

    return render(request, 'administracion/agregar_permisos_roles_usuario.html', {'usuario': usuario, 'form': form, 'redirect_url': redirect_url})

@rol_requerido('administrador')
@permiso_requerido
@login_required
def eliminar_permisos_roles_usuario(request, usuario_id):
    """
    Vista para eliminar permisos de los roles de un usuario existente.

    Esta vista permite a un administrador eliminar permisos de los roles de un usuario existente en el sistema.

    Parámetros:
        request (HttpRequest): La solicitud HTTP entrante.
        usuario_id (int): El ID del usuario del que se eliminarán permisos de sus roles.

    Retorna:
        HttpResponse: 
        Una respuesta HTTP que redirige al administrador a la gestión de usuarios
        después de eliminar los permisos de los roles del usuario especificado.

    """
    usuario = get_object_or_404(Usuario, id=usuario_id)
    roles_usuario = usuario.roles.all()
    permisos_seleccionados = None
    redirect_url = None
    if request.method == 'POST':
        form = EliminarPermisosForm(request.POST)
        if form.is_valid():
            permisos_seleccionados = form.cleaned_data['permisos']
            # Iterar sobre los roles del usuario y quitar permisos seleccionados
            for rol in roles_usuario:
                for permiso in permisos_seleccionados:
                    rol.permisos.remove(permiso)
            redirect_url = reverse('administracion:gestion_usuarios')
            messages.success(request, 'Permisos eliminados correctamente.')
    else:
        form = EliminarPermisosForm()

    return render(request, 'administracion/eliminar_permisos_roles_usuario.html', {
        'usuario': usuario,
        'roles_usuario': roles_usuario,
        'permisos_seleccionados': permisos_seleccionados,
        'form': form,
        'redirect_url': redirect_url
    })

@rol_requerido('administrador')
@permiso_requerido
@login_required
def crear_rol(request):
    
    """
    Vista para permitir a los administradores crear un nuevo rol en el sistema.

    El proceso de creación incluye la validación de un formulario. Si el formulario
    es válido, se procesa la creación del rol. Si hay algún error, se muestra un 
    mensaje indicando el problema.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la plantilla 'administracion/crear_rol.html' con el formulario 
        para agregar un rol y, si corresponde, mensajes de éxito o error.
    """
    
    redirect_url = None
    if request.method == 'POST':
        form = AgregarRolForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            
            nombre_minusculas = nombre.lower()  # Convierte todo a minúsculas
            nombre_mayuscula = nombre.capitalize()  # Pone la primera letra en mayúscula
            Rol.agregar_rol(nombre_minusculas, nombre_mayuscula)
            messages.success(request, 'El Rol se ha creado correctamente.')
            redirect_url = reverse('administracion:gestion_usuarios')
        else:
            messages.error(request, 'Hubo un problema al crear el Rol. Por favor, verifica los datos ingresados.')
            redirect_url = request.path
    else:
        form = AgregarRolForm()

    return render(request, 'administracion/crear_rol.html', {'form': form,'redirect_url': redirect_url})

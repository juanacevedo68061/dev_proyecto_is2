from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria
from .forms import CategoriaForm, AsignarPermisosForm, EliminarPermisosForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from roles.decorators import rol_requerido
from roles.models import Rol
from login.models import Usuario

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
@login_required
def listar_categorias(request):
    """
    Vista para listar categorías.

    Parámetros:
        request (HttpRequest): La solicitud HTTP entrante.

    Retorna:
        HttpResponse: Muestra la lista de categorías.
    """
    categorias = Categoria.objects.all()
    return render(request, 'administracion/listar_categorias.html', {'categorias': categorias})

@rol_requerido('administrador')
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
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'La categoría se ha creado correctamente.')
            return redirect('administracion:listar_categorias')
        else:
            messages.error(request, 'Hubo un problema al crear la categoría. Por favor, verifica los datos ingresados.')
    else:
        form = CategoriaForm()

    return render(request, 'administracion/crear_categoria.html', {'form': form})

@rol_requerido('administrador')
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
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'La categoría se ha actualizado correctamente.')
            return redirect('administracion:listar_categorias')
        else:
            messages.error(request, 'Hubo un problema al actualizar la categoría. Por favor, verifica los datos ingresados.')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'administracion/editar_categoria.html', {'form': form, 'categoria': categoria})

@rol_requerido('administrador')
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
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'La categoría se ha eliminado correctamente.')
        return redirect('administracion:listar_categorias')
    return render(request, 'administracion/eliminar_categoria.html', {'categoria': categoria})

@rol_requerido('administrador')
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
@login_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect('administracion:gestion_usuarios')

    return render(request, 'administracion/eliminar_usuario.html', {'usuario': usuario})

from roles.models import Rol

@rol_requerido('administrador')
@login_required
def asignar_roles_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
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
        return redirect('administracion:gestion_usuarios')

    return render(request, 'administracion/asignar_roles_usuario.html', {'usuario': usuario, 'roles_disponibles': roles_disponibles})



@rol_requerido('administrador')
@login_required
def eliminar_roles_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    if request.method == 'POST':
        roles_seleccionados = request.POST.getlist('roles')
        for rol_id in roles_seleccionados:
            rol = Rol.objects.get(id=rol_id)
            usuario.roles.remove(rol)
        messages.success(request, 'Roles eliminados correctamente.')
        return redirect('administracion:gestion_usuarios')

    roles_asignados = usuario.roles.all()
    return render(request, 'administracion/eliminar_roles_usuario.html', {'usuario': usuario, 'roles_asignados': roles_asignados})

def agregar_permisos_roles_usuario(request, usuario_id):
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

            return redirect('administracion:gestion_usuarios')
    else:
        form = AsignarPermisosForm(roles_asignados=roles_asignados)

    return render(request, 'administracion/agregar_permisos_roles_usuario.html', {'usuario': usuario, 'form': form})


@rol_requerido('administrador')
@login_required
def eliminar_permisos_roles_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    roles_usuario = usuario.roles.all()
    permisos_seleccionados = None

    if request.method == 'POST':
        form = EliminarPermisosForm(request.POST)
        if form.is_valid():
            permisos_seleccionados = form.cleaned_data['permisos']
            # Iterar sobre los roles del usuario y quitar permisos seleccionados
            for rol in roles_usuario:
                for permiso in permisos_seleccionados:
                    rol.permisos.remove(permiso)
            return redirect('administracion:gestion_usuarios')
    else:
        form = EliminarPermisosForm()

    return render(request, 'administracion/eliminar_permisos_roles_usuario.html', {
        'usuario': usuario,
        'roles_usuario': roles_usuario,
        'permisos_seleccionados': permisos_seleccionados,
        'form': form,
    })
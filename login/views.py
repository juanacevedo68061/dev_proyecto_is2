from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import FormularioRegistro, FormularioActualizarPerfil, FormularioActivarRol
from roles.models import Rol
from .models import Usuario

def inicio_sesion(request):
    """
    Vista para iniciar sesión de un usuario.

    Esta vista permite al usuario ingresar sus credenciales para iniciar sesión en el sistema.

    Parámetros:
        request: La solicitud HTTP entrante.

    Retorna:
        Redirecciona a la vista de perfil del usuario si el inicio de sesión es exitoso, 
        o muestra la página de inicio de sesión con mensajes de error.

    """
    if request.method == 'POST':
        formulario = AuthenticationForm(request, data=request.POST)
        if formulario.is_valid():
            nombre_usuario = formulario.cleaned_data.get('username')
            contraseña = formulario.cleaned_data.get('password')
            usuario = authenticate(username=nombre_usuario, password=contraseña)
            if usuario is not None:
                login(request, usuario)
                return redirect('/')
            else:
                messages.error(request, 'Credenciales inválidas. Por favor, inténtalo de nuevo.')
        else:
            messages.error(request, 'Por favor, corrige los errores a continuación.')
    else:
        formulario = AuthenticationForm()
    
    contexto = {'formulario': formulario}
    return render(request, 'login/inicio_sesion.html', contexto)

def registro(request):
    """
    Vista para registrar un nuevo usuario.

    Esta vista permite al usuario registrar una nueva cuenta proporcionando la información requerida.

    Parámetros:
        request: La solicitud HTTP entrante.

    Retorna:
        Redirecciona a la página de inicio de sesión después de un registro exitoso,
        o muestra la página de registro con mensajes de error.

    """
    if request.method == 'POST':
        formulario = FormularioRegistro(request.POST)
        if formulario.is_valid():
            formulario.save()
            nombre_usuario = formulario.cleaned_data.get('username')
            contraseña = formulario.cleaned_data.get('password1')
            usuario = authenticate(username=nombre_usuario, password=contraseña)
            login(request, usuario)
            return redirect('login:inicio_sesion')
        else:
            messages.error(request, 'Por favor, corrige los errores a continuación.')
    else:
        formulario = FormularioRegistro()
    
    contexto = {'formulario': formulario}
    return render(request, 'login/registro.html', contexto)

@login_required
def cerrar_sesion(request):
    """
    Vista para cerrar la sesión de un usuario.

    Esta vista cierra la sesión del usuario, vacía el campo 'rol_activado'
    y lo redirecciona a la página de inicio de sesión.

    Parámetros:
        request: La solicitud HTTP entrante.

    Retorna:
        Redirecciona a la página de inicio de sesión.

    """
    usuario = request.user
    usuario.rol_activo = None #vacia el rol_activo para que al iniciar sesion tenga que activarlo de vuelta.
    usuario.save()

    logout(request)
    return redirect('login:inicio_sesion')

@login_required
def activar_rol(request):
    """
    Vista para activar un rol para el usuario actual.

    Esta vista permite al usuario activar un rol específico, que será almacenado
    en el campo 'rol_activo' de su perfil de usuario.

    Parámetros:
        request: La solicitud HTTP entrante.

    Retorna:
        Redirecciona al perfil del usuario después de activar el rol.
    """
    if request.method == 'POST':
        rol_activo_id = request.POST['rol_activado']
        rol_activo = Rol.objects.get(pk=rol_activo_id)
        
        usuario = request.user
        usuario.rol_activo = rol_activo
        usuario.save()
        print("iniciooooooooooooooooooooooooo")
        if(usuario.rol_activo):
            print(usuario.rol_activo.nombre)
            print("en activar_rol si carga la activacion")
        
        messages.success(request, 'Rol activado exitosamente.')
    
    return redirect('login:perfil')

@login_required
def perfil_usuario(request):
    """
    Vista para mostrar y editar el perfil del usuario.

    Esta vista muestra el perfil del usuario, incluidos sus roles activos y la posibilidad de activar un rol adicional.
    Si el usuario no tiene roles, se muestra un mensaje correspondiente. Permite la actualización de información y cambio de contraseña.

    Parámetros:
        request: La solicitud HTTP entrante.

    Retorna:
        Renderiza la plantilla de perfil con el formulario y la información del usuario.    
    """
    usuario = request.user
    print("aquiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    if(usuario.rol_activo):
        print(usuario.rol_activo.nombre)
        print("DEBERIA HABER ACTIVADO ESTA MIERDERA")
    # Obtener roles del usuario
    roles = usuario.roles.all()
    mensaje_roles = 'No cuenta con ningún rol asignado.'
    
    # Si el usuario tiene roles, no mostramos el mensaje
    if roles:
        mensaje_roles = None

    # Si el usuario activó un rol, actualizar el objeto usuario
    rol_activado = request.GET.get('rol_activado')
    if rol_activado:
        rol_activado_obj = Rol.objects.get(pk=rol_activado)
        usuario.rol_activado = rol_activado_obj
        usuario.save()

    # Obtener formularios
    formulario = FormularioActualizarPerfil(instance=usuario)
    formulario_roles = FormularioActivarRol(instance=usuario)
    
    contexto = {
        'formulario': formulario,
        'formulario_roles': formulario_roles,
        'usuario': usuario,
        'roles': roles,
        'mensaje_roles': mensaje_roles,
    }
    print("MIRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    if(usuario.rol_activo):
        print(usuario.rol_activo.nombre)
        print("DEBERIA HABER ACTIVADO ESTA MIERDERA")
    
    return render(request, 'login/perfil_usuario.html', contexto)

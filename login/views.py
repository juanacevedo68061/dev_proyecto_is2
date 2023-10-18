from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import FormularioRegistro, FormularioActualizarPerfil
from publicaciones.models import Publicacion_solo_text
from django.urls import reverse
from django.http import JsonResponse

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
    redirect_url = None  # Variable para almacenar la URL de redirec
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
                redirect_url = request.path
        else:
            messages.error(request, 'Por favor, corrige los errores a continuación.')
            redirect_url = request.path
    else:
        formulario = AuthenticationForm()
    
    contexto = {'formulario': formulario,
                'redirect_url': redirect_url}
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
    redirect_url = None  # Variable para almacenar la URL de redirección
    if request.method == 'POST':
        formulario = FormularioRegistro(request.POST)
        if formulario.is_valid():
            formulario.save()
            nombre_usuario = formulario.cleaned_data.get('username')
            contraseña = formulario.cleaned_data.get('password1')
            usuario = authenticate(username=nombre_usuario, password=contraseña)
            login(request, usuario)
            messages.success(request, 'Registro exitoso.')
            redirect_url=reverse('login:inicio_sesion')
            
        else:
            messages.error(request, 'Por favor, corrige los errores a continuación.')
            redirect_url = request.path
    else:
        formulario = FormularioRegistro()
    
    contexto = {'formulario': formulario,'redirect_url': redirect_url}

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
    logout(request)
    return redirect('/')

@login_required
def perfil_usuario(request):
    """
    Vista para mostrar el perfil del usuario.
    Esta vista muestra el perfil del usuario, incluidos sus roles activos y la posibilidad de activar un rol adicional.
    Si el usuario no tiene roles, se muestra un mensaje correspondiente.
    Parámetros:
    request: La solicitud HTTP entrante.
    Retorna:
    Renderiza la plantilla de perfil con la información del usuario.
    """
    usuario = request.user

    # Obtener roles del usuario
    roles = usuario.roles.all()
    mensaje_roles = 'No cuenta con ningún rol asignado.'
    
    # Si el usuario tiene roles, no mostramos el mensaje
    if roles:
        mensaje_roles = None

    
    publicaciones = Publicacion_solo_text.objects.filter(autor=usuario)
    
    contexto = {
        'usuario': usuario,
        'roles': roles,
        'mensaje_roles': mensaje_roles,
        'publicaciones':publicaciones
    }
    
    return render(request, 'login/perfil_usuario.html', contexto)

@login_required
def perfil_actualizar(request):
    """
    Vista para actualizar el perfil del usuario.

    Esta vista permite al usuario actualizar su perfil, incluida la información y la contraseña.

    Parámetros:
        request: La solicitud HTTP entrante.

    Retorna:
        Redirecciona a la vista 'perfil_usuario' después de actualizar el perfil.
    """
    usuario = request.user

    if request.method == 'POST':
        formulario = FormularioActualizarPerfil(request.POST, instance=usuario)
        if formulario.is_valid():
            contraseña_actual = formulario.cleaned_data.get('contraseña_actual')
            if contraseña_actual and not usuario.check_password(contraseña_actual):
                messages.error(request, 'La contraseña actual no es correcta.')
            else:
                nueva_contraseña1 = formulario.cleaned_data.get('nueva_contraseña1')
                nueva_contraseña2 = formulario.cleaned_data.get('nueva_contraseña2')
                if nueva_contraseña1 and nueva_contraseña1 == nueva_contraseña2:
                    usuario.set_password(nueva_contraseña1)
                formulario.save()
                messages.success(request, 'Perfil actualizado exitosamente.')
                return redirect('login:perfil')
    else:
        formulario = FormularioActualizarPerfil(instance=usuario)

    contexto = {
        'formulario': formulario,
        'usuario': usuario,
    }

    return render(request, 'login/perfil_actualizar.html', contexto)

@login_required
def cargar_imagen(request):
    usuario = request.user

    if request.method == 'POST' and 'imagen' in request.FILES:
        usuario.imagen = request.FILES['imagen']
        usuario.save()
        return JsonResponse({'url': usuario.imagen.url})

    return JsonResponse({'error': 'No se pudo cargar la imagen'})

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Usuario
from roles.models import Rol

class FormularioCreacionUsuario(UserCreationForm):
    """
    Formulario para la creación de usuarios con campos de username, email y contraseña.
    """
    class Meta:
        model = Usuario
        fields = ('username', 'email')

class FormularioCambioUsuario(forms.ModelForm):
    """
    Formulario para el cambio de información de usuarios (username y email).
    """
    class Meta:
        model = Usuario
        fields = ('username', 'email')

class FormularioCambioContraseña(PasswordChangeForm):
    """
    Formulario para el cambio de contraseña de usuarios.
    """
    class Meta:
        model = Usuario

class FormularioRegistro(UserCreationForm):
    """
    Formulario de registro de usuarios con campos de username, email y contraseña.
    """
    email = forms.EmailField(label='Correo Electrónico', required=True)

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña'
        }

class FormularioActualizarPerfil(forms.ModelForm):
    """
    Formulario para la actualización del perfil de usuarios, incluyendo cambio de contraseña opcional.
    """
    nueva_contraseña1 = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput,
        required=False
    )
    nueva_contraseña2 = forms.CharField(
        label='Confirmar Nueva Contraseña',
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = Usuario
        fields = ('username', 'email')
        labels = {
            'username': 'Usuario',
            'email': 'Correo Electrónico'
        }

class FormularioActivarRol(forms.ModelForm):
    """Formulario para activar un rol para un usuario."""
    class Meta:
        model = Usuario
        fields = ['rol_activo']



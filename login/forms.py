from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django.core.exceptions import ValidationError

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
    contraseña_actual = forms.CharField(
        label='Contraseña Actual',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña Actual'}),
        required=True
    )
    nueva_contraseña1 = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nueva Contraseña'}),
        required=False
    )
    nueva_contraseña2 = forms.CharField(
        label='Confirmar Nueva Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Nueva Contraseña'}),
        required=False
    )
    
    class Meta:
        model = Usuario
        fields = ('username', 'email')
        labels = {
            'username': 'Usuario',
            'email': 'Correo Electrónico'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

from django import forms
from .models import Categoria
from login.models import Usuario
from roles.models import Rol
from django.contrib.auth.models import Permission

class CategoriaForm(forms.ModelForm):
    """
    Formulario para crear y editar una categoría.

    Este formulario se utiliza para ingresar información sobre una categoría,
    incluyendo su nombre y estado de moderación.

    Campos:
    -------
    nombre : str
        Nombre de la categoría.
    moderada : bool
        Estado de moderación de la categoría (True para moderada, False para no moderada).

    """

    class Meta:
        model = Categoria
        fields = ['nombre', 'moderada']

    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)

class AsignarPermisosForm(forms.Form):
    usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        widget=forms.HiddenInput(),
        required=False
    )
    rol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        label='Rol',
        required=True
    )
    permisos = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, roles_asignados=None, **kwargs):
        super(AsignarPermisosForm, self).__init__(*args, **kwargs)
        
        # Limitar las opciones de roles a los roles asignados al usuario
        if roles_asignados:
            self.fields['rol'].queryset = roles_asignados

        # Limitar las opciones de permisos a los permisos disponibles
        if roles_asignados:
            permisos_disponibles = Permission.objects.filter(rol__isnull=False).exclude(rol__in=roles_asignados)
            self.fields['permisos'].queryset = permisos_disponibles
            
class EliminarPermisosForm(forms.Form):
    permisos = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
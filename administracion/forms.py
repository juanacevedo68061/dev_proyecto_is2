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
    rol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        label='Rol',
        required=True
    )
    permisos = forms.MultipleChoiceField(
        choices=(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, roles_asignados=None, **kwargs):
        super(AsignarPermisosForm, self).__init__(*args, **kwargs)

        # Limitar las opciones de roles a los roles asignados al usuario
        if roles_asignados:
            self.fields['rol'].queryset = roles_asignados

        # Obtener todos los nombres de permisos en la clase Rol
        nombres_permisos_roles = []
        for rol_permisos in Rol.PERMISOS.values():
            nombres_permisos_roles.extend(rol_permisos)

        # Obtener los permisos asignados a los roles del usuario
        permisos_asignados = Permission.objects.filter(rol__in=roles_asignados).values_list('codename', flat=True)

        # Obtener los nombres de permisos disponibles excluyendo los ya asignados
        permisos_disponibles = set(nombres_permisos_roles) - set(permisos_asignados)

        # Configurar las opciones del campo permisos
        self.fields['permisos'].choices = [(nombre, nombre) for nombre in permisos_disponibles]

            
class EliminarPermisosForm(forms.Form):
    permisos = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
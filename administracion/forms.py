from django import forms
from .models import Categoria
from login.models import Usuario
from roles.models import Rol
from django.contrib.auth.models import Permission

class CategoriaForm(forms.ModelForm):
    """
    Formulario para crear y editar una categoría.

    Este formulario se utiliza para ingresar información sobre una categoría,
    incluyendo su nombre, descripción y estado de moderación.
    """

    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'moderada']

    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)

class AsignarPermisosForm(forms.Form):
    """
    Formulario para asignar permisos a roles de usuario.

    Este formulario se utiliza para asignar permisos específicos a roles de usuario
    en el sistema.
    """
    permisos = forms.MultipleChoiceField(
        choices=(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, roles_asignados=None, **kwargs):
        super(AsignarPermisosForm, self).__init__(*args, **kwargs)

        if roles_asignados:
            # Limitar las opciones de roles a los roles asignados al usuario
            self.fields['rol'] = forms.ModelChoiceField(
                queryset=roles_asignados,
                label='Rol',
                required=True
            )

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
        else:
            self.fields['rol'] = forms.ModelChoiceField(
                queryset=Rol.objects.none(),  # Si no hay roles asignados, no mostrar ningún rol
                label='Rol',
                required=True
            )
            
class EliminarPermisosForm(forms.Form):
    """
    Formulario para eliminar permisos de roles de usuario.

    Este formulario se utiliza para seleccionar y eliminar permisos de roles de usuario
    en el sistema.
    """
    permisos = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
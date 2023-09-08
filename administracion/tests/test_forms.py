from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from administracion.forms import CategoriaForm, AsignarPermisosForm, EliminarPermisosForm
from roles.models import Rol
from django.contrib.auth.models import Permission
from login.models import Usuario

class CategoriaFormTest(TestCase):
    def test_categoria_form_valid(self):
        data = {
            'nombre': 'Categoría de Prueba',
            'moderada': True,
        }
        form = CategoriaForm(data=data)
        self.assertTrue(form.is_valid())

    def test_categoria_form_invalid(self):
        data = {
            'nombre': '',
            'moderada': True,
        }
        form = CategoriaForm(data=data)
        self.assertFalse(form.is_valid())


class AsignarPermisosFormTest(TestCase):

    def setUp(self):
        # Crear un rol de prueba
        self.rol_prueba = Rol.objects.create(nombre='Rol de Prueba')

    def test_asignar_permisos_form_valid(self):
        # Crear un ContentType para tu modelo, reemplaza ModelClass con el modelo real
        content_type = ContentType.objects.get_for_model(Rol)

        # Crear permisos utilizando el ContentType
        permission1, created1 = Permission.objects.get_or_create(
            codename='permiso1',
            name='Permiso 1',
            content_type=content_type,
        )

        permission2, created2 = Permission.objects.get_or_create(
            codename='permiso2',
            name='Permiso 2',
            content_type=content_type,
        )

        roles_asignados = Rol.objects.filter(id=self.rol_prueba.id)

        form_data = {
            'rol': self.rol_prueba,
            'permisos': [permission1.codename, permission2.codename],
        }

        form = AsignarPermisosForm(data=form_data, roles_asignados=roles_asignados)

        self.assertTrue(form.is_valid())

    def test_asignar_permisos_form_invalid(self):
        # Crear un ContentType para tu modelo, reemplaza ModelClass con el modelo real
        content_type = ContentType.objects.get_for_model(Rol)

        # Crear permisos utilizando el ContentType
        permission1, created1 = Permission.objects.get_or_create(
            codename='permiso1',
            name='Permiso 1',
            content_type=content_type,
        )

        roles_asignados = Rol.objects.filter(id=self.rol_prueba.id)

        

        # Intentar asignar un permiso que no tiene el rol de prueba
        form_data = {
            'rol': self.rol_prueba,
            'permisos': ["rermiso3"],  # Nombre de un permiso que el rol de prueba no tiene
        }

        form = AsignarPermisosForm(data=form_data, roles_asignados=roles_asignados)

        

        self.assertFalse(form.is_valid())

class EliminarPermisosFormTest(TestCase):
    
    def setUp(self):
        # Crear un ContentType para tu modelo 'Rol'
        content_type = ContentType.objects.get_for_model(Rol)

        # Crear permisos utilizando el ContentType
        self.permiso1, created1 = Permission.objects.get_or_create(
            codename='permiso1',
            name='Permiso 1',
            content_type=content_type,
        )
        self.permiso2, created2 = Permission.objects.get_or_create(
            codename='permiso2',
            name='Permiso 2',
            content_type=content_type,
        )

        # Crear un rol de prueba
        self.rol_prueba = Rol.objects.create(nombre='Rol de Prueba')

    def test_eliminar_permisos_form_valid(self):
        # Asignar permisos al rol de prueba
        self.rol_prueba.permisos.add(self.permiso1, self.permiso2)

        # Obtener los permisos asociados al rol de prueba
        permisos_asociados = self.rol_prueba.permisos.all()

        # Crear datos del formulario para eliminar permisos
        form_data = {
            'permisos': [permiso.id for permiso in permisos_asociados],
        }

        form = EliminarPermisosForm(data=form_data)

        self.assertTrue(form.is_valid())

def test_eliminar_permisos_form_invalid(self):
    # Crear un ContentType para tu modelo 'Rol'
    content_type = ContentType.objects.get_for_model(Rol)

    # Crear permisos utilizando el ContentType
    self.permiso1, created1 = Permission.objects.get_or_create(
        codename='permiso1',
        name='Permiso 1',
        content_type=content_type,
    )
    self.permiso2, created2 = Permission.objects.get_or_create(
        codename='permiso2',
        name='Permiso 2',
        content_type=content_type,
    )

    # Intentar crear un permiso que no está asociado al 'Rol de Prueba'
    permiso_no_asociado, created = Permission.objects.get_or_create(
        codename='permiso3',
        name='Permiso 3',
        content_type=content_type,
    )

    # Crear datos del formulario para eliminar permisos
    form_data = {
        'permisos': [permiso_no_asociado.id],
    }

    form = EliminarPermisosForm(data=form_data)

    self.assertFalse(form.is_valid())

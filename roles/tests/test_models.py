from django.test import TestCase
from django.contrib.auth.models import Permission
from roles.models import Rol

class RolModelTest(TestCase):

    def test_creacion_de_roles_y_permisos(self):
        """
        Prueba que los roles se creen correctamente y que los permisos se asignen adecuadamente.
        """
        # Crea un rol de "autor"
        autor_rol = Rol.objects.create(nombre='autor')
        
        # Verifica que el rol se haya creado correctamente
        self.assertEqual(autor_rol.nombre, 'autor')

        # Verifica que los permisos correspondientes al rol de "autor" se hayan asignado
        permisos_autor = Permission.objects.filter(codename__in=['permiso1', 'permiso2'])
        for permiso in permisos_autor:
            self.assertTrue(permiso in autor_rol.permisos.all())

        # Crea un rol de "editor"
        editor_rol = Rol.objects.create(nombre='editor')

        # Verifica que el rol se haya creado correctamente
        self.assertEqual(editor_rol.nombre, 'editor')

        # Verifica que los permisos correspondientes al rol de "editor" se hayan asignado
        permisos_editor = Permission.objects.filter(codename__in=['permiso3', 'permiso4'])
        for permiso in permisos_editor:
            self.assertTrue(permiso in editor_rol.permisos.all())

        # Crea un rol de "publicador"
        publicador_rol = Rol.objects.create(nombre='publicador')

        # Verifica que el rol se haya creado correctamente
        self.assertEqual(publicador_rol.nombre, 'publicador')

        # Verifica que los permisos correspondientes al rol de "publicador" se hayan asignado
        permisos_publicador = Permission.objects.filter(codename__in=['permiso5', 'permiso6'])
        for permiso in permisos_publicador:
            self.assertTrue(permiso in publicador_rol.permisos.all())

        # Crea un rol de "administrador"
        administrador_rol = Rol.objects.create(nombre='administrador')

        # Verifica que el rol se haya creado correctamente
        self.assertEqual(administrador_rol.nombre, 'administrador')

        # Verifica que los permisos correspondientes al rol de "administrador" se hayan asignado
        permisos_administrador = Permission.objects.filter(codename__in=['permiso7', 'permiso8'])
        for permiso in permisos_administrador:
            self.assertTrue(permiso in administrador_rol.permisos.all())

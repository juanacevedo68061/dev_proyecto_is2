from django.test import TestCase
from login.models import Usuario
from roles.models import Rol

class UsuarioModeloTests(TestCase):
    """
    Pruebas para el modelo Usuario.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Configura los datos de prueba para todos los métodos de prueba en esta clase.
        """
        rol = Rol.objects.create(nombre='Rol de Prueba')
        Usuario.objects.create(username='usuario_prueba', suscriptor=True, rol_activo=rol)

    def test_str_metodo(self):
        """
        Prueba que el método __str__ del modelo devuelva el nombre de usuario correctamente.
        """
        usuario = Usuario.objects.get(id=1)
        self.assertEqual(str(usuario), 'usuario_prueba')

    def test_roles_asignados(self):
        """
        Prueba que los roles se puedan asignar y recuperar correctamente para un usuario.
        """
        usuario = Usuario.objects.get(id=1)
        rol = Rol.objects.get(id=1)
        usuario.roles.add(rol)
        self.assertTrue(rol in usuario.roles.all())

    def test_suscriptor_predeterminado(self):
        """
        Prueba que el campo suscriptor tiene el valor predeterminado correctamente.
        """
        usuario = Usuario.objects.get(id=1)
        self.assertTrue(usuario.suscriptor)

    def test_rol_activo(self):
        """
        Prueba que el campo rol_activo se establece y recupera correctamente para un usuario.
        """
        usuario = Usuario.objects.get(id=1)
        rol = Rol.objects.get(id=1)
        self.assertEqual(usuario.rol_activo, rol)

    def test_eliminar_rol_activo(self):
        """
        Prueba que el campo rol_activo se puede eliminar correctamente.
        """
        usuario = Usuario.objects.get(id=1)
        usuario.rol_activo = None
        usuario.save()
        self.assertIsNone(usuario.rol_activo)

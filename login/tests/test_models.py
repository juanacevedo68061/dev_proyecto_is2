from django.test import TestCase
from login.models import Usuario
from roles.models import Rol

class UsuarioModeloTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        rol = Rol.objects.create(nombre='Rol de Prueba')
        Usuario.objects.create(username='usuario_prueba', suscriptor=True, rol_activo=rol)

    def test_str_metodo(self):
        usuario = Usuario.objects.get(id=1)
        self.assertEqual(str(usuario), 'usuario_prueba')

    def test_roles_asignados(self):
        usuario = Usuario.objects.get(id=1)
        rol = Rol.objects.get(id=1)
        usuario.roles.add(rol)
        self.assertTrue(rol in usuario.roles.all())

    def test_suscriptor_predeterminado(self):
        usuario = Usuario.objects.get(id=1)
        self.assertTrue(usuario.suscriptor)

    def test_rol_activo(self):
        usuario = Usuario.objects.get(id=1)
        rol = Rol.objects.get(id=1)
        self.assertEqual(usuario.rol_activo, rol)

    def test_eliminar_rol_activo(self):
        usuario = Usuario.objects.get(id=1)
        usuario.rol_activo = None
        usuario.save()
        self.assertIsNone(usuario.rol_activo)

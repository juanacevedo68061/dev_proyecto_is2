from django.test import TestCase
from django.test.client import RequestFactory
from django.http import HttpResponse
from roles.decorators import rol_requerido
from login.models import Usuario 
from roles.models import Rol
from django.contrib.auth.decorators import login_required

class DecoratorTest(TestCase):
    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.factory = RequestFactory()
        self.user = Usuario.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.rol = Rol.objects.create(nombre='test_rol')
        self.user.roles.add(self.rol)

    def test_rol_requerido_acceso_permitido(self):
        """
        Prueba si el acceso está permitido para un usuario con el rol correcto.
        """
        @rol_requerido('test_rol')
        def view_func(request):
            return HttpResponse('Acceso permitido')

        request = self.factory.get('/')
        request.user = self.user

        response = view_func(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'Acceso permitido')


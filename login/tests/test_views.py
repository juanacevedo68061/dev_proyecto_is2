from django.test import TestCase, Client
from django.urls import reverse
from login.models import Usuario
from roles.models import Rol

class ViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Usuario.objects.create_user(username='usuario_prueba', password='contraseña123')
        self.rol = Rol.objects.create(nombre='Rol de Prueba')
        self.user.roles.add(self.rol)

    def test_inicio_sesion(self):
        """
        Prueba que la vista de inicio de sesión devuelve una respuesta exitosa (código 200)
        y utiliza la plantilla 'login/inicio_sesion.html'.
        """
        response = self.client.get(reverse('login:inicio_sesion'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/inicio_sesion.html')

    def test_registro(self):
        """
        Prueba que la vista de registro devuelve una respuesta exitosa (código 200)
        y utiliza la plantilla 'login/registro.html'.
        """
        response = self.client.get(reverse('login:registro'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/registro.html')

    def test_cerrar_sesion(self):
        """
        Prueba que la vista de cierre de sesión redirige al usuario a la vista de inicio de sesión después del cierre de sesión.
        """
        self.client.login(username='usuario_prueba', password='contraseña123')
        response = self.client.get(reverse('login:cerrar_sesion'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login:inicio_sesion'))

    def test_activar_rol(self):
        """
        Prueba que la vista de activación de rol redirige al usuario a la vista de perfil después de activar un rol.
        """
        self.client.login(username='usuario_prueba', password='contraseña123')
        response = self.client.post(reverse('login:activar_rol'), {'rol_activado': self.rol.id})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login:perfil'))

    def test_perfil_usuario(self):
        """
        Prueba que la vista de perfil de usuario devuelve una respuesta exitosa (código 200)
        y utiliza la plantilla 'login/perfil_usuario.html'.
        """
        self.client.login(username='usuario_prueba', password='contraseña123')
        response = self.client.get(reverse('login:perfil'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/perfil_usuario.html')

    def test_perfil_actualizar(self):
        """
        Prueba que la vista de actualización de perfil devuelve una respuesta exitosa (código 200)
        y utiliza la plantilla 'login/perfil_actualizar.html'.
        """
        self.client.login(username='usuario_prueba', password='contraseña123')
        response = self.client.get(reverse('login:perfil_actualizar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/perfil_actualizar.html')

    def test_perfil_actualizar_post(self):
        """
        Prueba que el formulario de actualización de perfil muestra errores cuando se envían datos vacíos.
        """
        self.client.login(username='usuario_prueba', password='contraseña123')
        response = self.client.post(reverse('login:perfil_actualizar'))
        self.assertEqual(response.status_code, 200)  # Prueba que el formulario no sea válido (por datos vacíos)
        self.assertTemplateUsed(response, 'login/perfil_actualizar.html')


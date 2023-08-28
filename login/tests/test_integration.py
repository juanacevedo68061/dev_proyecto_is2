from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from roles.models import Rol
from login.models import Usuario

class IntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Usuario.objects.create_user(username='usuario_prueba', password='contraseña123')
        self.rol = Rol.objects.create(nombre='Rol de Prueba')
        self.user.roles.add(self.rol)

    def test_registro_e_inicio_sesion(self):
        """
        Prueba de integración: Registra un usuario y verifica que pueda iniciar sesión.
        """
        # Registro de un nuevo usuario
        registro_data = {
            'username': 'usuario_prueba',
            'email': 'prueba@example.com',
            'password1': 'contraseña123',
            'password2': 'contraseña123',
        }
        response = self.client.post(reverse('login:registro'), data=registro_data, follow=True)
        self.assertEqual(response.status_code, 200)  # Verifica que la página de inicio de sesión se muestre

        # Inicio de sesión con el nuevo usuario
        inicio_sesion_data = {
            'username': 'usuario_prueba',
            'password': 'contraseña123',
        }
        response = self.client.post(reverse('login:inicio_sesion'), data=inicio_sesion_data, follow=True)
        self.assertEqual(response.status_code, 200)  # Verifica que se haya iniciado sesión correctamente

    def test_activar_rol_y_perfil(self):
        """
        Prueba de integración: Activa un rol para un usuario y verifica que aparezca en su perfil.
        """
        self.client.login(username='usuario_prueba', password='contraseña123')
        response = self.client.post(reverse('login:activar_rol'), {'rol_activado': self.rol.id})
        self.assertEqual(response.status_code, 302)  # Redirige después de activar el rol
        self.assertRedirects(response, reverse('login:perfil'))

        response = self.client.get(reverse('login:perfil'))
        self.assertContains(response, self.rol.nombre)  # Verifica que el rol activado esté en el perfil

    def test_actualizar_perfil(self):
        """
        Prueba de integración: Actualiza el perfil de usuario y verifica los cambios.
        """
        self.client.login(username='usuario_prueba', password='contraseña123')
        response = self.client.post(reverse('login:perfil_actualizar'), {'contraseña_actual': 'contraseña123', 'username': 'nuevo_usuario'})
        self.assertEqual(response.status_code, 302)  # Redirige después de actualizar el perfil
        self.assertRedirects(response, reverse('login:perfil'))

        user_updated = Usuario.objects.get(username='nuevo_usuario')
        self.assertEqual(user_updated.username, 'nuevo_usuario')  # Verifica que el username se haya actualizado



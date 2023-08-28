from django.test import TestCase
from django.urls import reverse
from .models import Usuario

class UsuarioTests(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
        }
        self.user = Usuario.objects.create_user(**self.user_data)

    def test_creacion_usuario(self):
        """Prueba la creación de un nuevo usuario personalizado."""
        self.assertEqual(self.user.username, self.user_data['username'])
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertTrue(self.user.check_password(self.user_data['password']))

    def test_vista_inicio_sesion(self):
        """Prueba la vista de inicio de sesión."""
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/inicio_sesion.html')

    def test_vista_perfil_usuario(self):
        """Prueba la vista de perfil de usuario."""
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        url = reverse('perfil')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/perfil_usuario.html')
        self.assertContains(response, self.user_data['username'])
        self.assertContains(response, self.user_data['email'])

    def test_vista_cerrar_sesion(self):
        """Prueba la vista de cierre de sesión."""
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        url = reverse('cerrar_sesion')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # 302 indica una redirección después del cierre de sesión
        self.assertRedirects(response, reverse('login'))

    def test_vista_registro(self):
        """Prueba la vista de registro."""
        url = reverse('registro')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/registro.html')

    def test_inicio_sesion_invalido(self):
        """Prueba el inicio de sesión inválido."""
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'contraseñaincorrecta',  # Contraseña incorrecta
        }

        response = self.client.post(url, data)
        messages = list(response.context['messages'])

        # Verifica el mensaje de error generado en la vista
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Por favor, corrige los errores a continuación.')

    def test_registro_invalido(self):
        """Prueba el registro inválido."""
        url = reverse('registro')
        data = {
            'username': '',                 # Usuario vacío (campo obligatorio)
            'password1': 'contraseña123',  # Contraseña
            'password2': 'contraseña456',  # Confirmación de contraseña no coincide
        }

        response = self.client.post(url, data)
        messages = list(response.context['messages'])

        # Verifica el mensaje de error generado en la vista
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Por favor, corrige los errores a continuación.')


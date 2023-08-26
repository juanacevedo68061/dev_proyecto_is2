from django.test import SimpleTestCase
from django.urls import reverse, resolve
from login import views

class UrlsTests(SimpleTestCase):
    def test_inicio_sesion_url_resuelta(self):
        """
        Prueba que la URL de inicio de sesión se resuelve a la función de vista correcta.
        """
        url = reverse('login:inicio_sesion')
        self.assertEqual(resolve(url).func, views.inicio_sesion)

    def test_registro_url_resuelta(self):
        """
        Prueba que la URL de registro se resuelve a la función de vista correcta.
        """
        url = reverse('login:registro')
        self.assertEqual(resolve(url).func, views.registro)

    def test_cerrar_sesion_url_resuelta(self):
        """
        Prueba que la URL de cierre de sesión se resuelve a la función de vista correcta.
        """
        url = reverse('login:cerrar_sesion')
        self.assertEqual(resolve(url).func, views.cerrar_sesion)

    def test_activar_rol_url_resuelta(self):
        """
        Prueba que la URL de activación de rol se resuelve a la función de vista correcta.
        """
        url = reverse('login:activar_rol')
        self.assertEqual(resolve(url).func, views.activar_rol)

    def test_perfil_usuario_url_resuelta(self):
        """
        Prueba que la URL de perfil de usuario se resuelve a la función de vista correcta.
        """
        url = reverse('login:perfil')
        self.assertEqual(resolve(url).func, views.perfil_usuario)

    def test_perfil_actualizar_url_resuelta(self):
        """
        Prueba que la URL de actualización de perfil se resuelve a la función de vista correcta.
        """
        url = reverse('login:perfil_actualizar')
        self.assertEqual(resolve(url).func, views.perfil_actualizar)

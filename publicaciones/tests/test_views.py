from .models import Publicacion_solo_text
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # Importa User si lo lo estás utilizando

class ViewsTests(TestCase):  
 
    def test_generar_qr_view(self):
        # Accede a la vista 'generar_qr' proporcionando el ID de la publicación
        response = self.client.get(reverse('generar_qr', args=[self.publicacion.id]))

        # Verifica que la respuesta sea un código de estado HTTP 200 (éxito)
        self.assertEqual(response.status_code, 200)

        # Verifica que el tipo de contenido sea 'image/png'
        self.assertEqual(response['Content-Type'], 'image/png')

  
    def test_compartidas_view(self):
        # Obtiene el contador de compartidas antes de realizar la solicitud
        compartidas_anteriores = self.publicacion.shared

        # Realiza una solicitud a la vista 'compartidas' proporcionando el ID de la publicación
        response = self.client.get(reverse('compartidas', args=[self.publicacion.id]))

        # Verifica que la respuesta sea un código de estado HTTP 200 (éxito)
        self.assertEqual(response.status_code, 200)

        # Verifica que la respuesta sea en formato JSON
        self.assertEqual(response['Content-Type'], 'application/json')

        # Analiza la respuesta JSON para obtener la cantidad de compartidas
        data = response.json()
        cantidad_compartidas = data['shared_count']

        # Verifica que la cantidad de compartidas haya aumentado en 1
        self.assertEqual(cantidad_compartidas, compartidas_anteriores + 1)
    
    
    def test_vista_auxiliar_email_view(self):
        # Establece la configuración del correo electrónico en el valor deseado
        settings.EMAIL_HOST_USER = 'correo@ejemplo.com'

        # Realiza una solicitud a la vista 'vista_auxiliar_email' proporcionando el ID de la publicación
        response = self.client.get(reverse('vista_auxiliar_email', args=[self.publicacion.id]))

        # Verifica que la respuesta sea un código de estado HTTP 200 (éxito)
        self.assertEqual(response.status_code, 200)

        # Verifica que la vista está utilizando la plantilla 'email.html'
        self.assertTemplateUsed(response, 'publicaciones/email.html')

        # Verifica que el contexto de la vista contiene la información esperada
        self.assertEqual(response.context['publicacion'], self.publicacion)
        self.assertEqual(response.context['cambio'], 3)  # Verifica el valor esperado
        self.assertEqual(response.context['razon'], 'No cumple con nuestras normas de seguridad')
        self.assertEqual(response.context['from_email'], 'correo@ejemplo.com')

        # Restaura la configuración del correo electrónico después de las pruebas
        settings.EMAIL_HOST_USER = ''


    @login_required
    def test_estado_view(self):
        # Inicia sesión como el usuario de prueba
        self.client.login(username='testuser', password='testpassword')

        # Obtiene el estado actual de la publicación antes de realizar la solicitud
        estado_anterior = self.publicacion.activo

        # Realiza una solicitud a la vista 'estado' proporcionando el ID de la publicación
        response = self.client.get(reverse('estado', args=[self.publicacion.id]))

        # Verifica que la respuesta sea un código de estado HTTP 200 (éxito)
        self.assertEqual(response.status_code, 200)

        # Verifica que la respuesta sea en formato JSON
        self.assertEqual(response['Content-Type'], 'application/json')

        # Analiza la respuesta JSON para obtener el estado actual
        data = response.json()
        estado_actual = data['activo']

        # Verifica que el estado de la publicación haya cambiado
        self.assertNotEqual(estado_actual, estado_anterior)

    def test_estado_view_requires_login(self):
        # Realiza una solicitud a la vista 'estado' sin iniciar sesión
        response = self.client.get(reverse('estado', args=[self.publicacion.id]))

        # Verifica que la respuesta sea un código de estado HTTP 302 (redirección)
        self.assertEqual(response.status_code, 302)

        # Verifica que la respuesta redirige a la página de inicio de sesión
        self.assertRedirects(response, f'/accounts/login/?next={reverse("estado", args=[self.publicacion.id])}')

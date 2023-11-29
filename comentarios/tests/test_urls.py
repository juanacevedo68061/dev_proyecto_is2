from django.test import SimpleTestCase
from django.urls import reverse, resolve
from comentarios import views
import uuid

class TestUrls(SimpleTestCase):
    # Test para la URL de crear un comentario con un UUID válido.
    def test_comentar_url_resolves(self):
        # Genera un UUID válido para usar como argumento en la URL.
        test_uuid = uuid.uuid4()
        # Construye la URL usando el UUID generado.
        url = reverse('comentarios:comentar', args=[test_uuid])
        # Verifica que la URL resuelve a la vista correcta.
        self.assertEquals(resolve(url).func, views.comentar)

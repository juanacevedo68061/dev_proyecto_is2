from django.test import TestCase, Client
from django.urls import reverse
from login.models import Usuario
from publicaciones.models import Publicacion_solo_text
import uuid

class CanvanViewsTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = Usuario.objects.create_user(username='@usuario_prueba', password='contraseña123')
        self.publicacion_borrador = Publicacion_solo_text.objects.create(
            titulo='Publicación de prueba',
            texto='<p>Contenido de prueba</p>',
            autor=self.user,
            estado='borrador',
            id_publicacion=uuid.uuid4()
        )
        self.publicacion_revision = Publicacion_solo_text.objects.create(
            titulo='Publicación en revisión',
            texto='<p>Contenido en revisión</p>',
            autor=self.user,
            estado='revision',
            id_publicacion=uuid.uuid4()
        )

    def test_canvas_autor(self):
        self.client.login(username='@usuario_prueba', password='contraseña123')
        response = self.client.get(reverse('canvan:canvas-autor'))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_canvas_editor(self):
        self.client.login(username='@usuario_prueba', password='contraseña123')
        response = self.client.get(reverse('canvan:canvas-editor'))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_canvas_publicador(self):
        self.client.login(username='@usuario_prueba', password='contraseña123')
        response = self.client.get(reverse('canvan:canvas-publicador'))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
from django.test import TestCase
from .models import Publicacion_solo_text
from login.models import Usuario
from administracion.models import Categoria

class Publicacion_solo_textTest(TestCase):
    def setUp(self):
        # Configuramos datos de prueba
        self.usuario = Usuario.objects.create(username='testuser', password='testpassword')
        self.categoria = Categoria.objects.create(nombre='TestCategory')
        self.publicacion = Publicacion_solo_text.objects.create(
            activo=True,
            titulo='Título de prueba',
            texto='Contenido de prueba',
            autor=self.usuario,
            estado='publicar',
            categoria=self.categoria,
            palabras_clave='prueba',
        )

    def test_publicacion_str(self):
        self.assertEqual(str(self.publicacion), 'Título de prueba')
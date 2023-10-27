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

    def test_get_absolute_url(self):
        expected_url = f'http://testserver/publicaciones/mostrar_publicacion/{self.publicacion.id_publicacion}/'
        self.assertEqual(self.publicacion.get_absolute_url(), expected_url)

    def test_likes_and_dislikes(self):
        # Verificamos que los valores iniciales sean correctos
        self.assertEqual(self.publicacion.likes, 0)
        self.assertEqual(self.publicacion.dislikes, 0)

        # Simulamos que un usuario da like y dislike
        user1 = Usuario.objects.create(username='user1', password='password1')
        user2 = Usuario.objects.create(username='user2', password='password2')

        self.publicacion.like_usuario.add(user1)
        self.publicacion.dislike_usuario.add(user2)

        # Verificamos que los valores se actualizan correctamente
        self.assertEqual(self.publicacion.likes, 1)
        self.assertEqual(self.publicacion.dislikes, 1)

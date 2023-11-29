from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from publicaciones.models import Publicacion_solo_text
from comentarios.models import Comment
import json

class ComentarioViewsTest(TestCase):

    def setUp(self):
        # Crear un usuario para las pruebas
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

        # Crear una publicación de prueba
        # Asegúrate de que los campos coincidan con lo que tu modelo Publicacion_solo_text espera
        self.publicacion = Publicacion_solo_text.objects.create(
            # Aquí se asume que tu modelo tiene los campos 'texto' y 'autor'
            texto='Texto de prueba', 
            autor=self.user  # Utiliza el usuario de prueba como el autor de la publicación
        )
        self.publicacion_id = self.publicacion.id_publicacion

        # Crear una URL para la vista 'comentar'
        self.comentar_url = reverse('comentarios:comentar', kwargs={'publicacion_id': self.publicacion_id})

        # Crear un comentario para probar la función de respuesta
        self.comentario = Comment.objects.create(
            usuario=self.user,
            publicacion_id=self.publicacion_id,
            texto='Comentario de prueba'
        )
        self.comentario_id = self.comentario.id
        self.responder_url = reverse('comentarios:responder', kwargs={'comentario_id': self.comentario_id})

    def test_comentar_view(self):
        # Enviar una solicitud POST a la vista 'comentar'
        response = self.client.post(self.comentar_url, {'texto': 'Nuevo comentario'})
        # Decodificar la respuesta JSON
        response_data = json.loads(response.content)

        # Verificar que la respuesta es exitosa
        self.assertTrue(response_data['success'])

    def test_responder_view(self):
        # Enviar una solicitud POST a la vista 'responder'
        response = self.client.post(self.responder_url, {'respuesta_texto': 'Respuesta al comentario'})
        # Decodificar la respuesta JSON
        response_data = json.loads(response.content)

        # Verificar que la respuesta es exitosa
        self.assertTrue(response_data['success'])
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from .models import Publicacion_solo_text, Categoria
from .views import kanban

class KanbanViewTest(TestCase):
    def setUp(self):
        # Creamos una instancia de la fábrica de solicitudes
        self.factory = RequestFactory()
        # Opcional: si necesitas un usuario para el test (debido al decorador @login_required)
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword'
        )

        # Crear datos mock para las pruebas
        self.categoria = Categoria.objects.create(moderada=True, ... )  # Agrega campos adicionales si los tiene
        Publicacion_solo_text.objects.create(estado='borrador', activo=True, categoria=self.categoria, ...)
        # Agrega más objetos Publicacion_solo_text si lo necesitas

    def test_kanban_view(self):
        # Creamos una solicitud GET mock
        request = self.factory.get('/ruta-a-tu-vista-kanban/')

        # Simulamos que un usuario está autenticado
        request.user = self.user

        # Usamos la función de vista kanban para obtener una respuesta
        response = kanban(request)

        # Validamos que la respuesta tenga un código 200 (éxito)
        self.assertEqual(response.status_code, 200)

        # Aquí puedes agregar más aserciones para validar el contenido del contexto o el contenido de la respuesta
        self.assertTrue('publicaciones_borrador' in response.context)
        # y así sucesivamente para otras claves en el contexto

        # Otras aserciones que podrías querer hacer
        # self.assertIn('algún texto esperado', response.content.decode())

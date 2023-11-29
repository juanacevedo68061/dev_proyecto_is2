from django.test import TestCase
from django.contrib.auth import get_user_model
from comentarios.models import Comment
from django.utils import timezone
import uuid

# Define una clase de prueba para el modelo Comment
class CommentModelTest(TestCase):

    # Método setUp que se ejecuta antes de cada método de prueba.
    # Se utiliza para configurar cualquier estado inicial para las pruebas.
    def setUp(self):
        # Obtener el modelo de usuario para crear una instancia de usuario para la prueba.
        User = get_user_model()
        # Crear un usuario de prueba para asociar con el comentario.
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Crear un comentario de prueba y guardarlo en la base de datos de prueba.
        self.comment = Comment.objects.create(
            usuario=self.user,
            publicacion_id=uuid.uuid4(),  # Genera un UUID único para la publicación.
            texto='Este es un comentario de prueba',
            fecha_creacion=timezone.now(),  # Asigna la fecha y hora actual.
        )

    # Prueba para verificar que la creación de una instancia del modelo Comment es correcta.
    def test_comment_creation(self):
        # Verifica que el comentario es una instancia del modelo Comment.
        self.assertTrue(isinstance(self.comment, Comment))

        # Verifica que la representación de cadena (__str__) es la esperada.
        self.assertEqual(self.comment.__str__(), f'{self.user.username} - {self.comment.texto[:20]}')

        # Verifica que la fecha de creación es una instancia de datetime.
        self.assertIsInstance(self.comment.fecha_creacion, type(timezone.now()))

        # Verifica que el comentario no tiene un comentario padre al momento de la creación.
        self.assertIsNone(self.comment.comentario_padre)

    # Prueba para verificar la relación padre-hijo de los comentarios (es decir, comentarios anidados).
    def test_comment_parent_relationship(self):
        # Crear un comentario hijo que se relacione con el comentario original.
        child_comment = Comment.objects.create(
            usuario=self.user,
            publicacion_id=uuid.uuid4(),
            texto='Este es un comentario hijo',
            comentario_padre=self.comment  # Establece el comentario original como padre.
        )

        # Verifica que el comentario hijo tiene el comentario original como padre.
        self.assertEqual(child_comment.comentario_padre, self.comment)

# Nota: Asegúrate de que la aplicación 'login' con el modelo 'Usuario' esté correctamente configurada
# y que el modelo 'Comment' esté definido en tu aplicación. Además, este código debe ejecutarse
# en el contexto de un entorno de Django configurado, lo que significa que no se ejecutará correctamente
# en esta plataforma de chat interactiva.

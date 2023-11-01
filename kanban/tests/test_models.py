from django.test import TestCase
from kanban.models import Registro
from login.models import Usuario
from roles.models import Rol

class RegistroModelTest(TestCase):

    def setUp(self):
        # Creamos una instancia de Usuario y Rol para usarla en el test
        self.usuario = Usuario.objects.create(username='testuser', password='testpassword123')
        self.rol = Rol.objects.create(nombre='testrol')

    def test_registro_creation(self):
        # Creamos una instancia de Registro
        registro = Registro.objects.create(
            publicacion_titulo='Test Publicacion',
            responsable=self.usuario
        )
        registro.roles.add(self.rol)

        # Verificamos que se haya creado correctamente
        self.assertEqual(Registro.objects.count(), 1)
        self.assertEqual(registro.publicacion_titulo, 'Test Publicacion')
        self.assertEqual(registro.responsable, self.usuario)
        self.assertIn(self.rol, registro.roles.all())
        self.assertIsNotNone(registro.fecha_cambio)

    def test_str_method(self):
        # Creamos una instancia de Registro
        registro = Registro.objects.create(
            publicacion_titulo='Test Publicacion',
            responsable=self.usuario
        )
        # Verificamos el método __str__
        self.assertEqual(str(registro), f'Registro de Test Publicacion por {self.usuario}')


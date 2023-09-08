from django.test import TestCase
from administracion.models import Categoria
from django.db.utils import IntegrityError

class CategoriaModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Configuración de objetos de prueba una vez para todos los métodos de prueba.
        Categoria.objects.create(nombre='Tecnología', moderada=True)

    def test_nombre_max_length(self):
        categoria = Categoria.objects.get(id=1)
        max_length = categoria._meta.get_field('nombre').max_length
        self.assertEquals(max_length, 100)

    def test_nombre_unique(self):
        # Crea una categoría con un nombre único
        categoria = Categoria.objects.create(nombre="Nombre Único", moderada=True)

        # Intenta crear otra categoría con el mismo nombre (debería generar IntegrityError)
        with self.assertRaises(IntegrityError) as context:
            Categoria.objects.create(nombre="Nombre Único", moderada=True)

        # Verifica que el error sea de tipo IntegrityError
        self.assertIn('UNIQUE constraint', str(context.exception))

    def test_moderada_default(self):
        categoria = Categoria.objects.get(id=1)
        self.assertTrue(categoria.moderada)

    def test_str_representation(self):
        categoria = Categoria.objects.get(id=1)
        self.assertEqual(str(categoria), 'Tecnología')

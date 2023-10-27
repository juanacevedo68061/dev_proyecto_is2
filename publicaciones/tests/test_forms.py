from django.test import TestCase
from administracion.models import Categoria
from .forms import PublicacionForm, BusquedaAvanzadaForm
from .models import Publicacion_solo_text

class PublicacionFormTest(TestCase):

    def setUp(self):
        self.categoria_suscriptor = Categoria.objects.create(nombre="Suscriptor", suscriptores=True, moderada=True)
        self.categoria_no_suscriptor = Categoria.objects.create(nombre="No Suscriptor", suscriptores=False, moderada=False)

    def test_valid_form(self):
        data = {
            'titulo': 'Test titulo',
            'texto': 'Test texto',
            'palabras_clave': 'test, prueba',
            'categoria_suscriptores': self.categoria_suscriptor.id,
            'categoria_no_suscriptores': self.categoria_no_suscriptor.id,
            'vigencia': True,
            'vigencia_unidad': 'd',
            'vigencia_cantidad': 1,
            'programar': True,
            'programar_unidad': 'h',
            'programar_cantidad': 2,
        }
        form = PublicacionForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_vigencia(self):
        data = {
            'titulo': 'Test titulo',
            'texto': 'Test texto',
            'palabras_clave': 'test, prueba',
            'categoria_suscriptores': self.categoria_suscriptor.id,
            'vigencia': True,
        }
        form = PublicacionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('vigencia_unidad', form.errors)
        self.assertIn('vigencia_cantidad', form.errors)

    def test_invalid_programar(self):
        data = {
            'titulo': 'Test titulo',
            'texto': 'Test texto',
            'palabras_clave': 'test, prueba',
            'categoria_suscriptores': self.categoria_suscriptor.id,
            'programar': True,
        }
        form = PublicacionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('programar_unidad', form.errors)
        self.assertIn('programar_cantidad', form.errors)

class BusquedaAvanzadaFormTest(TestCase):

    def setUp(self):
        self.categoria1 = Categoria.objects.create(nombre="Cat1", suscriptores=True)
        self.categoria2 = Categoria.objects.create(nombre="Cat2", suscriptores=False)

    def test_valid_form_anonimo(self):
        data = {
            'q': 'test',
            'categorias': [self.categoria2.id],
            'fecha_publicacion': '2023-01-01',
            'autor': 'Autor Test',
        }
        form = BusquedaAvanzadaForm(anonimo=True, data=data)
        self.assertTrue(form.is_valid())

    def test_valid_form_no_anonimo(self):
        data = {
            'q': 'test',
            'categorias': [self.categoria1.id, self.categoria2.id],
            'fecha_publicacion': '2023-01-01',
            'autor': 'Autor Test',
        }
        form = BusquedaAvanzadaForm(anonimo=False, data=data)
        self.assertTrue(form.is_valid())


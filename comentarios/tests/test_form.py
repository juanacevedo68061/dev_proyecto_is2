from django.test import TestCase
from comentarios.forms import CommentForm


class CommentFormTest(TestCase):

    # Test para verificar la inicialización correcta del formulario
    def test_form_initialization(self):
        # Crear una instancia del formulario
        form = CommentForm()
        # Verificar que el campo 'id_texto' esté inicializado correctamente
        self.assertEqual(form.fields['id_texto'].widget.attrs['id'], 'id_texto')
        # Verificar que el campo 'id_texto' no sea obligatorio
        self.assertFalse(form.fields['id_texto'].required)

    # Test para verificar la validación del formulario con datos válidos
    def test_valid_data(self):
        # Crear datos de prueba para el formulario
        data = {'texto': 'Este es un comentario de prueba', 'id_texto': ''}
        # Crear una instancia del formulario con datos de prueba
        form = CommentForm(data=data)
        # Verificar que el formulario sea válido
        self.assertTrue(form.is_valid())

    # Test para verificar el comportamiento del formulario con datos inválidos
    def test_invalid_data(self):
        # Crear datos de prueba inválidos para el formulario
        data = {'texto': '', 'id_texto': ''}
        # Crear una instancia del formulario con datos inválidos
        form = CommentForm(data=data)
        # Verificar que el formulario no sea válido
        self.assertFalse(form.is_valid())

from django.test import TestCase
from django.forms import CharField, Textarea
from froala_editor.widgets import FroalaEditor
from django.conf import settings

class FroalaFieldTestCase(TestCase):
    def test_froala_field_formfield(self):
        # Verifica que cuando USE_FROALA_EDITOR está habilitado, el widget sea FroalaEditor.
        settings.USE_FROALA_EDITOR = True
        froala_field = FroalaField()
        formfield = froala_field.formfield()
        self.assertIsInstance(formfield.widget, FroalaEditor)

    def test_froala_field_formfield_textarea(self):
        # Verifica que cuando USE_FROALA_EDITOR está deshabilitado, el widget sea Textarea.
        settings.USE_FROALA_EDITOR = False
        froala_field = FroalaField()
        formfield = froala_field.formfield()
        self.assertIsInstance(formfield.widget, Textarea)

    def test_froala_field_options(self):
        # Verifica que las opciones pasadas al campo se establecen correctamente en el widget.
        settings.USE_FROALA_EDITOR = True
        options = {'key': 'value'}
        froala_field = FroalaField(options=options)
        formfield = froala_field.formfield()
        self.assertEqual(formfield.widget.options, options)


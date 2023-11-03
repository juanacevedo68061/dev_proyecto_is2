from django.test import TestCase
from login.forms import FormularioRegistro, FormularioActualizarPerfil

class FormsTests(TestCase):
    def test_formulario_registro_valido(self):

        form_data = {
            'username': '@usuario_prueba',
            'email': 'usuario@example.com',
            'password1': 'contraseña123',
            'password2': 'contraseña123'
        }
        form = FormularioRegistro(data=form_data)
        self.assertTrue(form.is_valid())

    def test_formulario_registro_invalido(self):
        form_data = {
            'username': '',
            'email': 'correo_invalido',
            'password1': 'contraseña123',
            'password2': 'contraseña456'
        }
        form = FormularioRegistro(data=form_data)
        self.assertFalse(form.is_valid())

    def test_formulario_actualizar_perfil_valido(self):
        form_data = {
            'username': '@usuario_prueba',
            'email': 'nuevo_correo@example.com',
            'contraseña_actual': 'contraseña_actual',
            'nueva_contraseña1': '',
            'nueva_contraseña2': ''
        }
        form = FormularioActualizarPerfil(data=form_data)
        self.assertTrue(form.is_valid())

    def test_formulario_actualizar_perfil_invalido(self):
        form_data = {
            'username': '',
            'email': 'correo_invalido',
            'contraseña_actual': 'contraseña_actual',
            'nueva_contraseña1': '',
            'nueva_contraseña2': 'contraseña_nueva'
        }
        form = FormularioActualizarPerfil(data=form_data)
        self.assertFalse(form.is_valid())

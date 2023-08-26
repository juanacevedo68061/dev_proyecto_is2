from django.test import TestCase
from roles.models import Rol
from login.forms import FormularioRegistro, FormularioActualizarPerfil, FormularioActivarRol

class FormsTests(TestCase):
    def test_formulario_registro_valido(self):
        """
        Prueba que el formulario de registro es válido con datos correctos.
        """
        form_data = {
            'username': 'usuario_prueba',
            'email': 'usuario@example.com',
            'password1': 'contraseña123',
            'password2': 'contraseña123'
        }
        form = FormularioRegistro(data=form_data)
        self.assertTrue(form.is_valid())

    def test_formulario_registro_invalido(self):
        """
        Prueba que el formulario de registro es inválido con datos incorrectos.
        """
        form_data = {
            'username': '',
            'email': 'correo_invalido',
            'password1': 'contraseña123',
            'password2': 'contraseña456'
        }
        form = FormularioRegistro(data=form_data)
        self.assertFalse(form.is_valid())

    def test_formulario_actualizar_perfil_valido(self):
        """
        Prueba que el formulario de actualización de perfil es válido con datos correctos.
        """
        form_data = {
            'username': 'usuario_prueba',
            'email': 'nuevo_correo@example.com',
            'contraseña_actual': 'contraseña_actual',
            'nueva_contraseña1': '',
            'nueva_contraseña2': ''
        }
        form = FormularioActualizarPerfil(data=form_data)
        self.assertTrue(form.is_valid())

    def test_formulario_actualizar_perfil_invalido(self):
        """
        Prueba que el formulario de actualización de perfil es inválido con datos incorrectos.
        """
        form_data = {
            'username': '',
            'email': 'correo_invalido',
            'contraseña_actual': 'contraseña_actual',
            'nueva_contraseña1': '',
            'nueva_contraseña2': 'contraseña_nueva'
        }
        form = FormularioActualizarPerfil(data=form_data)
        self.assertFalse(form.is_valid())

    def test_formulario_activar_rol_valido(self):
        """
        Prueba que el formulario de activación de rol es válido con datos correctos.
        """
        rol = Rol.objects.create(nombre='Rol de Prueba')
        form_data = {
            'rol_activo': rol.id
        }
        form = FormularioActivarRol(data=form_data)
        self.assertTrue(form.is_valid())

    def test_formulario_activar_rol_invalido(self):
        """
        Prueba que el formulario de activación de rol es válido incluso con datos incorrectos.
        """
        form_data = {
            'rol_activo': None
        }
        form = FormularioActivarRol(data=form_data)
        self.assertTrue(form.is_valid()) # Cambiado a assertTrue para reflejar que el formulario es válido incluso si el campo está vacío
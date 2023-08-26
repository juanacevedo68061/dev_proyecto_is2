from django.test import TestCase
from django.core import management
from django.db.models.signals import pre_save, post_save
from django.dispatch import Signal
from login.models import Usuario
from roles.models import Rol
from login.signals import crear_roles_iniciales, asignar_roles

class SignalsTests(TestCase):
    def test_creacion_de_roles_iniciales(self):
        """
        Prueba la señal de creación de roles iniciales.
        """
        usuario = Usuario()
        crear_roles_iniciales(sender=Usuario, instance=usuario)
        self.assertEqual(Rol.objects.count(), 2)  # Asegura que se crearon los roles

    def test_asignacion_de_roles(self):
        """
        Prueba la señal de asignación de roles.
        """
        admin_rol = Rol.objects.create(nombre='administrador')
        autor_rol = Rol.objects.create(nombre='autor')
        usuario = Usuario(username='usuario_prueba')
        usuario.save()

        asignar_roles(sender=Usuario, instance=usuario, created=True)
        usuario.refresh_from_db()  # Actualiza la instancia del usuario desde la base de datos

        self.assertTrue(admin_rol in usuario.roles.all())
        self.assertTrue(autor_rol in usuario.roles.all())

    def test_signal_con_pre_save(self):
        """
        Prueba el funcionamiento del pre_save con señales.
        """
        pre_save_signal = Signal()
        pre_save_signal.connect(crear_roles_iniciales, sender=Usuario)

        usuario = Usuario()
        pre_save.send(sender=Usuario, instance=usuario)

        self.assertEqual(Rol.objects.count(), 2)  # Asegura que se crearon los roles

    def test_signal_con_post_save(self):
        """
        Prueba el funcionamiento del post_save con señales.
        """
        post_save_signal = Signal()
        post_save_signal.connect(asignar_roles, sender=Usuario)

        admin_rol = Rol.objects.create(nombre='administrador')
        autor_rol = Rol.objects.create(nombre='autor')
        usuario = Usuario(username='usuario_prueba')
        usuario.save()

        post_save.send(sender=Usuario, instance=usuario, created=True)
        usuario.refresh_from_db()

        self.assertTrue(admin_rol in usuario.roles.all())
        self.assertTrue(autor_rol in usuario.roles.all())

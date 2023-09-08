from django.test import TestCase
from django.db.models.signals import post_save
from django.dispatch import Signal
from roles.models import Rol
from login.models import Usuario
from login.signals import asignar_roles

class SignalsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Define una señal personalizada para el post_save
        cls.post_save_signal = Signal()

        # Asocia el signal personalizado al modelo Usuario
        post_save.connect(asignar_roles, sender=Usuario)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Desconecta el signal personalizado después de las pruebas
        post_save.disconnect(asignar_roles, sender=Usuario)

    def test_asignar_roles_a_usuario_recien_creado(self):
        """
        Prueba que los roles se asignen correctamente a un usuario recién creado.
        """
        # Crea un nuevo usuario
        usuario = Usuario(username='usuario_prueba')
        usuario.save()

        # Refresca la instancia del usuario desde la base de datos
        usuario.refresh_from_db()

        # Verifica que el usuario tenga el rol de 'autor'
        autor_rol = Rol.objects.get(nombre='autor')
        self.assertTrue(autor_rol in usuario.roles.all())

        # Si es el primer usuario creado, verifica que también tenga el rol de 'administrador'
        if Usuario.objects.count() == 1:
            admin_rol = Rol.objects.get(nombre='administrador')
            self.assertTrue(admin_rol in usuario.roles.all())


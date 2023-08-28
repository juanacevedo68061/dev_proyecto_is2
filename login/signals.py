from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import Permission
from django.dispatch import receiver
from roles.models import Rol
from .models import Usuario


@receiver(pre_save, sender=Usuario)
def crear_roles_iniciales(sender, instance, **kwargs):
    """
    Crea los roles definidos en la clase Rol antes de que se cree el primer usuario,
    y agrega permisos específicos a cada rol.

    Parámetros:
        sender: Modelo que envía la señal (Usuario).
        instance: Instancia del usuario que se está creando o actualizando.
        kwargs: Argumentos adicionales (no se usan aquí).
    """
    # signals.py


from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from roles.models import Rol
from .models import Usuario


@receiver(pre_save, sender=Usuario)
def crear_roles_iniciales(sender, instance, **kwargs):
    """
    Crea los roles definidos en la clase Rol antes de que se cree el primer usuario,
    y agrega permisos específicos a cada rol.

    Parámetros:
    sender: Modelo que envía la señal (Usuario).
    instance: Instancia del usuario que se está creando o actualizando.
    kwargs: Argumentos adicionales (no se usan aquí).
    """
    if Usuario.objects.count() == 0:
        # Crear el rol de Administrador y agregar el permiso específico
        admin_rol, _ = Rol.objects.get_or_create(nombre='administrador')
        permiso_admin, _ = Permission.objects.get_or_create(
            codename='permiso_admin',
            name='Permiso Admin',
            content_type=ContentType.objects.get_for_model(Rol)  # Usar ContentType para el modelo Rol
        )
        admin_rol.permisos.add(permiso_admin)

        # Crear el rol de Autor y agregar el permiso específico
        autor_rol, _ = Rol.objects.get_or_create(nombre='autor')
        permiso_autor, _ = Permission.objects.get_or_create(
            codename='permiso_autor',
            name='Permiso Autor',
            content_type=ContentType.objects.get_for_model(Rol)  # Usar ContentType para el modelo Rol
        )
        autor_rol.permisos.add(permiso_autor)

        # Crear el rol de Editor y agregar el permiso específico
        editor_rol, _ = Rol.objects.get_or_create(nombre='editor')
        permiso_editor, _ = Permission.objects.get_or_create(
            codename='permiso_editor',
            name='Permiso Editor',
            content_type=ContentType.objects.get_for_model(Rol)  # Usar ContentType para el modelo Rol
        )
        editor_rol.permisos.add(permiso_editor)

        # Crear el rol de Publicador y agregar el permiso específico
        publicador_rol, _ = Rol.objects.get_or_create(nombre='publicador')
        permiso_publicador, _ = Permission.objects.get_or_create(
            codename='permiso_publicador',
            name='Permiso Publicador',
            content_type=ContentType.objects.get_for_model(Rol)  # Usar ContentType para el modelo Rol
        )
        publicador_rol.permisos.add(permiso_publicador)


@receiver(post_save, sender=Usuario)
def asignar_roles(sender, instance, created, **kwargs):
    """
    Asigna roles a un usuario recién creado.

    Parámetros:
        sender: Modelo que envía la señal (Usuario).
        instance: Instancia del usuario recién creado.
        created: True si se acaba de crear el usuario, False si se está actualizando.
    """
    if created:
        if Usuario.objects.count() == 1:  # Verificar si es el primer usuario registrado
            admin_rol = Rol.objects.get(nombre='administrador')
            instance.roles.add(admin_rol)

        autor_rol = Rol.objects.get(nombre='autor')
        instance.roles.add(autor_rol)

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from roles.models import Rol
from .models import Usuario

@receiver(pre_save, sender=Usuario)
def crear_roles_iniciales(sender, instance, **kwargs):
    """
    Crea los roles de 'Administrador' y 'Autor' antes de que se cree el primer usuario.

    Parámetros:
        sender: Modelo que envía la señal (Usuario).
        instance: Instancia del usuario que se está creando o actualizando.
        kwargs: Argumentos adicionales (no se usan aquí).
    """
    if Usuario.objects.count() == 0:
        # Crear el rol de Administrador y Autor
        admin_rol, _ = Rol.objects.get_or_create(nombre='administrador')
        autor_rol, _ = Rol.objects.get_or_create(nombre='autor')
        
        # Guardar los roles en la base de datos
        admin_rol.save()
        autor_rol.save()


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
        

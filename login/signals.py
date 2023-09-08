from django.db.models.signals import post_save
from django.dispatch import receiver
from roles.models import Rol
from .models import Usuario

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
        if Usuario.objects.count() == 1:
            admin_rol = Rol.objects.create(nombre='administrador')
            instance.roles.add(admin_rol)
            #print(f'Permisos del rol de Administrador: {admin_rol.permisos.all()}')

        autor_rol = Rol.objects.create(nombre='autor')
        instance.roles.add(autor_rol)
        #print(f'Permisos del rol de Autor: {autor_rol.permisos.all()}')
        

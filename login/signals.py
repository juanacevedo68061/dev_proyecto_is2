from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from roles.models import Rol  

User = get_user_model()

@receiver(post_save, sender=User)
def assign_roles(sender, instance, created, **kwargs):
    if created:
        autor_rol = Rol.objects.get(name='autor')  
        instance.roles.add(autor_rol)
        if User.objects.count() == 1:  # Verificar si es el primer usuario registrado
            admin_rol = Rol.objects.get(name='administrador')  
            instance.roles.add(admin_rol)


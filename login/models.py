from django.db import models
from django.contrib.auth.models import AbstractUser
from roles.models import Rol

class Usuario(AbstractUser):
    """
    Modelo personalizado de usuario que extiende AbstractUser.
    
    Atributos:
        roles (ManyToManyField): Roles asignados al usuario.
        suscriptor (BooleanField): Indica si el usuario es suscriptor.
        rol_activo (ForeignKey): El rol activo seleccionado por el usuario.

    Métodos:
        __str__: Representación en cadena del usuario (nombre de usuario).
    """
    roles = models.ManyToManyField(Rol, related_name='usuarios')
    suscriptor = models.BooleanField(default=False)
    rol_activo = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios_activos')

    def __str__(self):
        return self.username

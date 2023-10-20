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
    username = models.CharField(
        max_length=20,
        unique=True,
        help_text='Máximo 20 caracteres. Requerido. Letras, dígitos y @/./+/-/_ solamente.',
    )
    imagen = models.ImageField(upload_to='profile_images', blank=True, null=True)
    roles = models.ManyToManyField(Rol, related_name='usuarios')
    suscriptor = models.BooleanField(default=False)
    
    #def save(self, *args, **kwargs):
        # Eliminar todos los "@" de la cadena
        #self.username = self.username.replace('@', '')
        
        # Agregar "@" al principio
        #self.username = f'@{self.username}'
        
        #super(Usuario, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
    


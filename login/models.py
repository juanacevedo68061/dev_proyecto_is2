from django.db import models
from django.contrib.auth.models import AbstractUser
from roles.models import Rol

class Usuario(AbstractUser):
    roles = models.ManyToManyField(Rol, related_name='usuario')
    suscriptor = models.BooleanField(default=False) 

    def __str__(self):
        return self.username

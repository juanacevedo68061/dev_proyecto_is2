from django.db import models
from django.contrib.auth.models import Permission

class Rol(models.Model): 
    ROLES = (
        ('autor', 'Autor'),
        ('editor', 'Editor'),
        ('publicador', 'Publicador'),
        ('administrador', 'Administrador'),
    )

    name = models.CharField(max_length=20, choices=ROLES, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.get_name_display()



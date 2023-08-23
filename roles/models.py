from django.db import models
from django.contrib.auth.models import Permission

class Rol(models.Model): 
    """
    Modelo que representa los roles en el sistema.

    Atributos:
        nombre (CharField): El nombre del rol (Autor, Editor, Publicador, Administrador).
        permisos (ManyToManyField): Los permisos asignados a este rol.

    Métodos:
        crear_roles_iniciales: Crea los roles iniciales con un permiso cada uno después de la migración inicial.
    """
    ROLES = (
        ('autor', 'Autor'),
        ('editor', 'Editor'),
        ('publicador', 'Publicador'),
        ('administrador', 'Administrador'),
    )

    nombre = models.CharField(max_length=20, choices=ROLES, unique=True)
    permisos = models.ManyToManyField(Permission, blank=True)


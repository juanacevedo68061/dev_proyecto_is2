from django.db import models
from login.models import Usuario
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    """
    Modelo que representa una categoría para las publicaciones.

    Atributos:
        nombre (str): El nombre único de la categoría.
        moderada (bool): Indica si la categoría está moderada o no.

    Métodos:
        __str__(): Devuelve una representación de cadena del objeto, que es el nombre de la categoría.

    """

    nombre = models.CharField(max_length=100, unique=True)
    moderada = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


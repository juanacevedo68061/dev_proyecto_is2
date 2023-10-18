from django.db import models

class Categoria(models.Model):
    """
    Modelo que representa una categoría para las publicaciones.

    Atributos:
        nombre (str): El nombre único de la categoría.
        moderada (bool): Indica si la categoría está moderada o no.
        descripcion (str): Una descripción de la categoría.

    Métodos:
        __str__(): Devuelve una representación de cadena del objeto, que es el nombre de la categoría.

    """

    nombre = models.CharField(max_length=30, unique=True)
    moderada = models.BooleanField(default=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

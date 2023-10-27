from django.db import models
import secrets

def get_random_color():
    while True:
        color = f'#{secrets.token_hex(3)}'
        if color != '#FFFFFF' and not Categoria.objects.filter(color=color).exists():
            return color

class Categoria(models.Model):
    """
    Modelo que representa una categoría para las publicaciones.

    Atributos:
        nombre (str): El nombre único de la categoría.
        moderada (bool): Indica si la categoría está moderada o no.
        descripcion (str): Una descripción de la categoría.
        color (str): Color único asignado a la categoría.

    Métodos:
        __str__(): Devuelve una representación de cadena del objeto, que es el nombre de la categoría.

    """
    nombre = models.CharField(max_length=30, unique=True)
    moderada = models.BooleanField(default=False)
    descripcion = models.TextField(blank=True, null=True)
    suscriptores = models.BooleanField(default=False)
    color = models.CharField(max_length=7, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.color:
            self.color = get_random_color()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
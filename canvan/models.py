#modelo provisorio, aun esta muy incompleto
from django.db import models
from publicaciones.models import Publicacion  # Importar el modelo Publicacion de la aplicación publicaciones
from roles.models import Rol  # Importar el modelo Rol de la aplicación roles

class Canvan(models.Model):
    ESTADOS_VISUALIZACION = [
        ('autor', 'Autor'),
        ('editor', 'Editor'),
        ('publicador', 'Publicador'),
    ]

    publicaciones = models.ManyToManyField(Publicacion)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    estado_visualizacion = models.CharField(max_length=20, choices=ESTADOS_VISUALIZACION)

    def __str__(self):
        return f"Canvan de {self.rol}"


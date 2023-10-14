from django.db import models
from login.models import Usuario
import uuid

class Registro(models.Model):
    CANVAS_CHOICES = [
        ('autor', 'Autor'),
        ('editor', 'Editor'),
        ('publicador', 'Publicador'),
    ]

    publicacion_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)
    publicacion_titulo = models.CharField(max_length=255)
    nuevo_estado = models.CharField(max_length=20)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    canvas = models.CharField(max_length=20, choices=CANVAS_CHOICES)
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Registro de {self.publicacion_titulo} en {self.get_canvas_display()} por {self.usuario}'

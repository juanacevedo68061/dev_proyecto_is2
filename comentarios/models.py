from django.db import models
from login.models import Usuario
from django.utils import timezone
import uuid

class Comment(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    publicacion_id = models.UUIDField(default=uuid.uuid4, editable=False)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    comentario_padre = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='respuestas')
    editado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.usuario.username} - {self.texto[:20]}'

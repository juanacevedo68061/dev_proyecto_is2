from django.db import models
from login.models import Usuario
import uuid
from roles.models import Rol

class Registro(models.Model):
    publicacion_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)
    publicacion_titulo = models.CharField(max_length=255)
    anterior = models.CharField(max_length=20 , blank=True, null=True)
    nuevo = models.CharField(max_length=20 , blank=True, null=True)
    responsable = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True)
    roles = models.ManyToManyField(Rol, related_name='roles_responsable')
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Registro de {self.publicacion_titulo} por {self.responsable}'

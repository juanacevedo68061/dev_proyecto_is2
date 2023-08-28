from django.db import models
from login.models import Usuario
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    """
    La clase categoria contiene el campo nombre y contiene un campo booleano que indica si la misma es moderada o no
    nombre = models.CharField(max_length=100)
    moderada = models.BooleanField(default=True)
    """
    
    def __str__(self):
        return self.nombre


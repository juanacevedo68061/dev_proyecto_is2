from django.db import models
from login.models import Usuario
import uuid
from roles.models import Rol

class Registro(models.Model):
    """
    Clase que representa un registro de cambios en el sistema Kanban.

    Atributos:
    -----------
    publicacion_id : UUIDField
        ID único de la publicación.
    
    publicacion_titulo : CharField
        Título de la publicación.
    
    anterior : CharField, opcional
        Estado anterior de la publicación.
    
    nuevo : CharField, opcional
        Nuevo estado de la publicación.
    
    responsable : ForeignKey a Usuario, opcional
        Usuario responsable del cambio.
    
    roles : ManyToManyField a Rol, opcional
        Roles relacionados con el cambio.
    
    fecha_cambio : DateTimeField
        Fecha y hora del cambio.
    """
    publicacion_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)
    publicacion_titulo = models.CharField(max_length=255)
    anterior = models.CharField(max_length=20 , blank=True, null=True)
    nuevo = models.CharField(max_length=20 , blank=True, null=True)
    responsable = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True)
    roles = models.ManyToManyField(Rol, related_name='roles_responsable')
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Método que devuelve una representación de cadena del registro.

        Returns:
        --------
        str
            Representación de cadena del registro.
        """       
        return f'Registro de {self.publicacion_titulo} por {self.responsable}'

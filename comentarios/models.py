from django.db import models
from login.models import Usuario
from django.utils import timezone
import uuid

class Comment(models.Model):
    """
    Modelo que representa un comentario en el sistema.

    Atributos:
        usuario (ForeignKey): Referencia al usuario que ha hecho el comentario.
                             Relaciona con el modelo Usuario.
        publicacion_id (UUIDField): Identificador único para cada publicación, 
                                    generado automáticamente usando uuid.uuid4.
        texto (TextField): Contenido del comentario.
        fecha_creacion (DateTimeField): Fecha y hora de creación del comentario, 
                                        establecida automáticamente al momento de la creación.
        comentario_padre (ForeignKey): Referencia opcional a otro comentario, 
                                       estableciendo una relación jerárquica entre comentarios.
                                       Puede ser `null` o `blank`. Relaciona consigo mismo y 
                                       utiliza `related_name='padre'`.

    Métodos:
        __str__: Devuelve una representación en cadena del comentario, mostrando el nombre 
                 de usuario y los primeros 20 caracteres del texto del comentario.
    """

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    publicacion_id = models.UUIDField(default=uuid.uuid4, editable=False)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    comentario_padre = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='padre')

    def __str__(self):
        return f'{self.usuario.username} - {self.texto[:20]}'

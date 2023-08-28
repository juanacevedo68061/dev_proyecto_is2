from django.db import models
from login.models import Usuario
from administracion.models import Categoria
from django.core.exceptions import ValidationError
#from ckeditor.fields import RichTextField 
#da error porque aun falta descargar archivos estaticos para que funcione
#ya despues se le debe agregar lo necesario, todo esta en la documentacion.

class Publicacion(models.Model):
    """
    Modelo que representa una publicación en el sistema.
    """
    ESTADOS_CONTENIDO = [
        ('borrador', 'Borrador'),
        ('revision', 'Revisión'),
        ('publicar', 'Publicar'),
        ('publicado', 'Publicado'),
        ('rechazado', 'Rechazado'),
        ('inactivo', 'Inactivo'),
    ]

    TIPOS_PUBLICACION = [
        ('rich_text', 'Rich Text'),
        ('solo_text', 'Solo Text'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPOS_PUBLICACION)
    resumen = models.TextField()
    id_publicacion = models.CharField(max_length=20)
    share = models.BooleanField(default=False)
    codigo_qr = models.ImageField(upload_to='codigos_qr/', blank=True)
    imagen_thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    version = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=20, choices=ESTADOS_CONTENIDO, default='borrador')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    programar_publicacion = models.DateTimeField(null=True, blank=True)
    vigencia_publicacion = models.DateTimeField(null=True, blank=True)
    suscriptores_exclusivos = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    palabras_clave = models.CharField(max_length=100, blank=True)
    likes = models.ManyToManyField(Usuario, related_name='publicaciones_liked', blank=True)
    dislikes = models.ManyToManyField(Usuario, related_name='publicaciones_disliked', blank=True)

    def __str__(self):
        """
        Devuelve una representación en forma de cadena del resumen de la publicación.
        """
        return self.resumen


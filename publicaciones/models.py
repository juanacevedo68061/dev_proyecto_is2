from django.db import models
from login.models import Usuario
from administracion.models import Categoria
from tinymce.models import HTMLField
from django.urls import reverse
import uuid

class Publicacion_solo_text(models.Model):
    ESTADOS_CONTENIDO = [
        ('borrador', 'Borrador'),
        ('revision', 'Revisión'),
        ('publicar', 'Publicar'),
        ('publicado', 'Publicado'),
    ]

    activo = models.BooleanField(default=True)
    titulo = models.CharField(max_length=200, blank=True, null=True)
    #texto = models.TextField()
    texto = HTMLField()
    id_publicacion = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    url_publicacion = models.CharField(max_length=200, blank=True, null=True)
    codigo_qr = models.ImageField(upload_to='codigos_qr/', blank=True)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    version = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=20, choices=ESTADOS_CONTENIDO)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    programar_publicacion = models.DateTimeField(null=True, blank=True)
    vigencia_publicacion = models.DateTimeField(null=True, blank=True)
    suscriptores_exclusivos = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=True, null=True)
    palabras_clave = models.CharField(max_length=100, blank=True)
    likes = models.ManyToManyField(Usuario, related_name='publicaciones_liked', blank=True)
    dislikes = models.ManyToManyField(Usuario, related_name='publicaciones_disliked', blank=True)
    share = models.ManyToManyField(Usuario, related_name='publicaciones_shared', blank=True)

    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('publicaciones:mostrar_publicacion', args=[str(self.id_publicacion)])



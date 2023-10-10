from django.db import models
from login.models import Usuario
from administracion.models import Categoria
from tinymce.models import HTMLField
from django.urls import reverse
import uuid
from django.conf import settings

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
    likes = models.PositiveIntegerField(default=0)
    like_usuario = models.ManyToManyField(Usuario, blank=True, related_name='publicaciones_likes')
    dislikes = models.PositiveIntegerField(default=0)
    dislike_usuario = models.ManyToManyField(Usuario, blank=True, related_name='publicaciones_dislikes')
    comments = models.PositiveIntegerField(default=0)
    shared = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        domain = f'{settings.SITE_DOMAIN}:{settings.SITE_PORT}'
        path = reverse('publicaciones:mostrar_publicacion', args=[str(self.id_publicacion)])
        url= f'http://{domain}{path}'
        return url
    



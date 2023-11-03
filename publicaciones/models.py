from django.db import models
from login.models import Usuario
from administracion.models import Categoria
from tinymce.models import HTMLField
from django.urls import reverse
import uuid
from django.conf import settings
from django.utils import timezone
import datetime
from django_comments_xtd.moderation import moderator, XtdCommentModerator


class Calificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE,blank=True, null=True)
    rating = models.PositiveIntegerField(default=0)

class Publicacion_solo_text(models.Model):
    ESTADOS_CONTENIDO = [
        ('borrador', 'Borrador'),
        ('revision', 'Revisión'),
        ('publicar', 'Publicar'),
        ('publicado', 'Publicado'),
        ('rechazado', 'Rechazado'),
    ]

    UNIDADES_TIEMPO = (
        ('d', 'Días'),
        ('h', 'Horas'),
        ('m', 'Minutos'),
    )

    COLORES = [
        ('rojo', 'Rojo'),
        ('amarillo', 'Amarillo'),
        ('verde', 'Verde'),
    ]

    activo = models.BooleanField(default=True)
    titulo = models.CharField(max_length=200, blank=True, null=True)
    texto = HTMLField()
    id_publicacion = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    url_publicacion = models.CharField(max_length=200, blank=True, null=True)
    codigo_qr = models.ImageField(upload_to='codigos_qr/', blank=True)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    version = models.PositiveIntegerField(default=1)    
    estado = models.CharField(max_length=20, choices=ESTADOS_CONTENIDO, null=True, blank=True)
    para_editor = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_publicacion = models.DateField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=True, null=True)
    palabras_clave = models.CharField(max_length=100, blank=True)
    likes = models.PositiveIntegerField(default=0)
    like_usuario = models.ManyToManyField(Usuario, blank=True, related_name='publicaciones_likes')
    dislikes = models.PositiveIntegerField(default=0)
    dislike_usuario = models.ManyToManyField(Usuario, blank=True, related_name='publicaciones_dislikes')
    views = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    shared = models.PositiveIntegerField(default=0)
    semaforo = models.CharField(max_length=9, choices=COLORES, default='rojo')
    calificaciones = models.ManyToManyField(Calificacion, blank=True, related_name='publicaciones_calificaciones')
    calificaciones_cantidad = models.PositiveIntegerField(default=0)

    vigencia = models.BooleanField(default=False)
    vigencia_tiempo = models.DateTimeField(null=True, blank=True)
    vigencia_unidad = models.CharField(max_length=1, choices=UNIDADES_TIEMPO, null=True, blank=True)
    vigencia_cantidad = models.PositiveIntegerField(null=True, blank=True)
    
    programar = models.BooleanField(default=False)
    programar_tiempo = models.DateTimeField(null=True, blank=True)
    programar_unidad = models.CharField(max_length=1, choices=UNIDADES_TIEMPO, null=True, blank=True)
    programar_cantidad = models.PositiveIntegerField(null=True, blank=True)

    def get_absolute_url(self):
        domain = f'{settings.SITE_DOMAIN}:{settings.SITE_PORT}'
        path = reverse('publicaciones:mostrar_publicacion', args=[str(self.id_publicacion)])
        url= f'http://{domain}{path}'
        return url

    def calcular_vigencia(self):
        if self.vigencia_unidad and self.vigencia_cantidad:
            if self.vigencia_unidad == 'd':
                delta = datetime.timedelta(days=self.vigencia_cantidad)
            elif self.vigencia_unidad == 'h':
                delta = datetime.timedelta(hours=self.vigencia_cantidad)
            else:
                delta = datetime.timedelta(minutes=self.vigencia_cantidad)
            
            self.vigencia_tiempo = timezone.now() + delta
            self.save()
            print(self.vigencia_tiempo)
    
    def calcular_programar(self):
        if self.programar_unidad and self.programar_cantidad:
            if self.programar_unidad == 'd':
                delta = datetime.timedelta(days=self.programar_cantidad)
            elif self.programar_unidad == 'h':
                delta = datetime.timedelta(hours=self.programar_cantidad)
            else:
                delta = datetime.timedelta(minutes=self.programar_cantidad)
            
            self.programar_tiempo = timezone.now() + delta
            self.save()

    def save(self, *args, **kwargs):
        original = None
        
        if self.id_publicacion:
            try:
                original = Publicacion_solo_text.objects.get(id_publicacion=self.id_publicacion)
            except Publicacion_solo_text.DoesNotExist:
                original = None

        if original:
            if (
                self.titulo != original.titulo or
                self.texto != original.texto or
                self.palabras_clave != original.palabras_clave or
                self.categoria != original.categoria or
                self.estado != original.estado
            ):
                self.version += 1

        super(Publicacion_solo_text, self).save(*args, **kwargs)


    def __str__(self):
        return self.titulo
    
class PublicacionCommentModerator(XtdCommentModerator):
    email_notification = True  # Si quieres notificaciones por correo electrónico

moderator.register(Publicacion_solo_text, PublicacionCommentModerator)
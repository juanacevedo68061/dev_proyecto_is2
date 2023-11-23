from django.db import models
from login.models import Usuario
from administracion.models import Categoria
from froala_editor.fields import FroalaField
from django.urls import reverse
import uuid
from django.conf import settings
from django.utils import timezone
import datetime
from django_comments_xtd.moderation import moderator, XtdCommentModerator


class Calificacion(models.Model):
    """
    Modelo que representa las calificaciones de una publicación.

    Atributos:
    -----------
    usuario : ForeignKey a Usuario
        El usuario que ha realizado la calificación.
    rating : PositiveIntegerField
        El valor de la calificación (puede ser 0 o más).

    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE,blank=True, null=True)
    rating = models.PositiveIntegerField(default=0)

class Publicacion_solo_text(models.Model):
    """
    Modelo que representa una publicación de texto en el sistema.

    Atributos:
    -----------
    activo : BooleanField
        Indica si la publicación está activa o no.
    titulo : CharField, opcional
        El título de la publicación.
    texto : HTMLField
        El contenido HTML de la publicación.
    id_publicacion : UUIDField
        ID único de la publicación.
    url_publicacion : CharField, opcional
        La URL de la publicación.
    codigo_qr : ImageField, opcional
        La imagen del código QR asociado a la publicación.
    autor : ForeignKey a Usuario
        El autor de la publicación.
    version : PositiveIntegerField
        La versión de la publicación.
    estado : CharField, choices=ESTADOS_CONTENIDO, opcional
        El estado de la publicación (borrador, revisión, publicar, publicado, rechazado).
    para_editor : BooleanField
        Indica si la publicación está destinada a un editor.
    fecha_creacion : DateTimeField
        La fecha de creación de la publicación.
    fecha_publicacion : DateField, opcional
        La fecha de publicación de la publicación.
    categoria : ForeignKey a Categoria, opcional
        La categoría a la que pertenece la publicación.
    palabras_clave : CharField, opcional
        Las palabras clave asociadas a la publicación.
    likes : PositiveIntegerField
        La cantidad de "me gusta" recibidos por la publicación.
    like_usuario : ManyToManyField a Usuario
        Los usuarios que han dado "me gusta" a la publicación.
    dislikes : PositiveIntegerField
        La cantidad de "no me gusta" recibidos por la publicación.
    dislike_usuario : ManyToManyField a Usuario
        Los usuarios que han dado "no me gusta" a la publicación.
    views : PositiveIntegerField
        La cantidad de visualizaciones de la publicación.
    comments : PositiveIntegerField
        La cantidad de comentarios en la publicación.
    shared : PositiveIntegerField
        La cantidad de veces que la publicación ha sido compartida.
    semaforo : CharField, choices=COLORES
        El estado del semáforo asociado a la publicación (rojo, amarillo, verde).
    calificaciones : ManyToManyField a Calificacion
        Las calificaciones asociadas a la publicación.
    calificaciones_cantidad : PositiveIntegerField
        La cantidad total de calificaciones recibidas.

    vigencia : BooleanField
        Indica si la publicación tiene una fecha de vigencia programada.
    vigencia_tiempo : DateTimeField, opcional
        La fecha y hora en la que la publicación dejará de ser vigente.
    vigencia_unidad : CharField, choices=UNIDADES_TIEMPO, opcional
        La unidad de tiempo para la vigencia (días, horas, minutos).
    vigencia_cantidad : PositiveIntegerField, opcional
        La cantidad de tiempo para la vigencia.

    programar : BooleanField
        Indica si la publicación está programada para una fecha futura.
    programar_tiempo : DateTimeField, opcional
        La fecha y hora en la que la publicación será programada para su publicación.
    programar_unidad : CharField, choices=UNIDADES_TIEMPO, opcional
        La unidad de tiempo para la programación (días, horas, minutos).
    programar_cantidad : PositiveIntegerField, opcional
        La cantidad de tiempo para la programación.

    Métodos:
    --------
    get_absolute_url():
        Obtiene la URL absoluta de la publicación.
    calcular_vigencia():
        Calcula la fecha y hora de vigencia de la publicación.
    calcular_programar():
        Calcula la fecha y hora de programación de la publicación.
    save(`*args`, `**kwargs`):
        Método personalizado para guardar la publicación y gestionar su versión.

    """

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
    texto = FroalaField()
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
    destacado = models.BooleanField(default=False)

    vigencia = models.BooleanField(default=False)
    vigencia_tiempo = models.DateTimeField(null=True, blank=True)
    vigencia_unidad = models.CharField(max_length=1, choices=UNIDADES_TIEMPO, null=True, blank=True)
    vigencia_cantidad = models.PositiveIntegerField(null=True, blank=True)
    
    programar = models.BooleanField(default=False)
    programar_tiempo = models.DateTimeField(null=True, blank=True)
    programar_unidad = models.CharField(max_length=1, choices=UNIDADES_TIEMPO, null=True, blank=True)
    programar_cantidad = models.PositiveIntegerField(null=True, blank=True)

    def get_absolute_url(self):
        """
        Obtiene la URL absoluta de la publicación.

        Returns:
        --------
        str
            La URL absoluta de la publicación.
        """
        domain = f'{settings.SITE_DOMAIN}:{settings.SITE_PORT}'
        path = reverse('publicaciones:mostrar_publicacion', args=[str(self.id_publicacion)])
        url= f'http://{domain}{path}'
        return url

    def calcular_vigencia(self):
        """
        Calcula la fecha y hora de vigencia de la publicación.
        """
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
        """
        Calcula la fecha y hora de programación de la publicación.
        """
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
        """
        Método personalizado para guardar la publicación y gestionar su versión.

        Si la publicación ya existe, aumenta la versión si hay cambios en los atributos específicos.

        Parameters:
        -----------
        `*args`, `**kwargs`:
            Argumentos adicionales para el método de guardar.
        """
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
        """
        Devuelve una representación en cadena del título de la publicación.

        Returns:
        --------
        str
            Representación en cadena del título de la publicación.
        """
        return self.titulo
    
class PublicacionCommentModerator(XtdCommentModerator):
    email_notification = True  # Si quieres notificaciones por correo electrónico

moderator.register(Publicacion_solo_text, PublicacionCommentModerator)
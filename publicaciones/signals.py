from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Publicacion_solo_text

@receiver(post_save, sender=Publicacion_solo_text)
def actualizar_destacado(sender, instance, **kwargs):
    instance.actualizar_destacado()

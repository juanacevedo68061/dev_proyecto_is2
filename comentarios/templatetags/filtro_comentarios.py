from django import template
from comentarios.models import Comment

register = template.Library()

@register.simple_tag
def respuestas(comentario_id):
    return Comment.objects.filter(comentario_padre_id=comentario_id)

@register.simple_tag
def cantidad(comentario_id):
    return Comment.objects.filter(comentario_padre_id=comentario_id).count()

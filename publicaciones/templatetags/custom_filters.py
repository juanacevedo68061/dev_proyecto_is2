from django import template
import re

register = template.Library()

@register.filter
def find_image_url(html_text):
    # Utilizamos una expresión regular para encontrar la URL de la imagen en el contenido HTML
    img_tag = re.search(r'<img.*?src=["\'](https?://.*?)(?=["\'])', html_text)
    if img_tag:
        return img_tag.group(1)
    else:
        return None

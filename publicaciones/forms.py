# En forms.py
from django import forms
from .models import Publicacion_solo_text

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion_solo_text
        fields = ['titulo', 'texto', 'categoria', 'palabras_clave']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo'].widget.attrs.update({'class': 'form-control', 'id': 'id_titulo'})
        self.fields['texto'].widget.attrs.update({'class': 'form-control', 'id': 'id_texto', 'rows': '4'})
        self.fields['categoria'].widget.attrs.update({'class': 'form-control', 'id': 'id_categoria'})
        self.fields['palabras_clave'].widget.attrs.update({'class': 'form-control', 'id': 'id_palabras_clave'})
        self.fields['titulo'].label = 'Título'
        self.fields['texto'].label = 'Texto'
        self.fields['categoria'].label = 'Categoría'
        self.fields['palabras_clave'].label = 'Palabras Clave'


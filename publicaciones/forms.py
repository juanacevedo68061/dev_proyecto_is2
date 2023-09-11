# En forms.py
from django import forms
from .models import Publicacion

class PublicacionForm(forms.ModelForm):
    datos_parciales = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Publicacion
        fields = ['titulo', 'tipo', 'resumen', 'imagen', 'categoria', 'palabras_clave']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo'].widget.attrs.update({'class': 'form-control', 'id': 'id_titulo', 'required': True})
        self.fields['tipo'].widget.attrs.update({'class': 'form-control', 'id': 'id_tipo'})
        self.fields['resumen'].widget.attrs.update({'class': 'form-control', 'id': 'id_resumen', 'rows': '4', 'required': True})
        self.fields['imagen'].widget.attrs.update({'class': 'form-control-file', 'id': 'id_imagen'})
        self.fields['categoria'].widget.attrs.update({'class': 'form-control', 'id': 'id_categoria'})
        self.fields['palabras_clave'].widget.attrs.update({'class': 'form-control', 'id': 'id_palabras_clave'})

        self.fields['titulo'].label = 'Título'
        self.fields['tipo'].label = 'Tipo de Publicación'
        self.fields['resumen'].label = 'Resumen'
        self.fields['imagen'].label = 'Imagen Principal'
        self.fields['categoria'].label = 'Categoría'
        self.fields['palabras_clave'].label = 'Palabras Clave'

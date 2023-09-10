# En forms.py
from django import forms
from .models import Publicacion

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['titulo', 'tipo', 'resumen', 'categoria', 'palabras_clave']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super(PublicacionForm, self).__init__(*args, **kwargs)

        self.fields['titulo'].widget.attrs['class'] = 'form-control'
        self.fields['tipo'].widget.attrs['class'] = 'form-control'
        self.fields['resumen'].widget.attrs['class'] = 'form-control'
        self.fields['categoria'].widget.attrs['class'] = 'form-control'
        self.fields['palabras_clave'].widget.attrs['class'] = 'form-control'
        self.fields['titulo'].widget.attrs['placeholder'] = 'Escribe el título de la publicación'
        self.fields['tipo'].widget.attrs['placeholder'] = 'Selecciona el tipo de publicación'
        self.fields['resumen'].widget.attrs['placeholder'] = 'Escribe un resumen de la publicación'
        self.fields['categoria'].widget.attrs['placeholder'] = 'Selecciona la categoría'
        self.fields['palabras_clave'].widget.attrs['placeholder'] = 'Agrega palabras clave separadas por comas'

        if instance:
            self.fields['titulo'].initial = instance.titulo
            self.fields['tipo'].initial = instance.tipo
            self.fields['resumen'].initial = instance.resumen
            self.fields['categoria'].initial = instance.categoria
            self.fields['palabras_clave'].initial = instance.palabras_clave

    def clean_resumen(self):
        resumen = self.cleaned_data.get('resumen')
        if len(resumen) < 10:
            raise forms.ValidationError('El resumen debe tener al menos 10 caracteres.')
        return resumen



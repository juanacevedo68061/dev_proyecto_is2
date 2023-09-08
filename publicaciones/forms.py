from django import forms
from .models import Publicacion

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['tipo', 'resumen', 'categoria', 'palabras_clave']

    def __init__(self, *args, **kwargs):
        super(PublicacionForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].widget.attrs['class'] = 'form-control'
        self.fields['resumen'].widget.attrs['class'] = 'form-control'
        self.fields['categoria'].widget.attrs['class'] = 'form-control'
        self.fields['palabras_clave'].widget.attrs['class'] = 'form-control'
        self.fields['tipo'].widget.attrs['placeholder'] = 'Selecciona el tipo de publicación'
        self.fields['resumen'].widget.attrs['placeholder'] = 'Escribe un resumen de la publicación'
        self.fields['categoria'].widget.attrs['placeholder'] = 'Selecciona la categoría'
        self.fields['palabras_clave'].widget.attrs['placeholder'] = 'Agrega palabras clave separadas por comas'

    def clean_resumen(self):
        resumen = self.cleaned_data.get('resumen')
        if len(resumen) < 10:
            raise forms.ValidationError('El resumen debe tener al menos 10 caracteres.')
        return resumen


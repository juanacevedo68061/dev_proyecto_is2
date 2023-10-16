# En forms.py
from .models import Categoria  # Importa el modelo de categoría
from administracion.models import Categoria  # Importa el modelo de categoría
from django import forms
from .models import Publicacion_solo_text


class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion_solo_text
        fields = ['titulo', 'texto', 'categoria', 'palabras_clave']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo'].widget.attrs.update(
            {'class': 'form-control', 'id': 'id_titulo'})
        self.fields['texto'].widget.attrs.update(
            {'class': 'form-control', 'id': 'id_texto', 'rows': '4'})
        self.fields['categoria'].widget.attrs.update(
            {'class': 'form-control', 'id': 'id_categoria'})
        self.fields['palabras_clave'].widget.attrs.update(
            {'class': 'form-control', 'id': 'id_palabras_clave'})
        self.fields['titulo'].label = 'Título'
        self.fields['texto'].label = 'Texto'
        self.fields['categoria'].label = 'Categoría'
        self.fields['palabras_clave'].label = 'Palabras Clave'


class BusquedaAvanzadaForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'id': 'id_q'}),
    )

    categorias = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[],  # Aquí proporcionaremos las opciones de categorías dinámicamente
    )
    fecha_publicacion = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    autor = forms.CharField(
        required=False,
        max_length=100,  # Ajusta la longitud máxima según tus necesidades
    )

    def __init__(self, *args, **kwargs):
        super(BusquedaAvanzadaForm, self).__init__(*args, **kwargs)

        # Cargar las opciones de categorías dinámicamente desde la base de datos
        categorias_disponibles = Categoria.objects.all()
        self.fields['categorias'].choices = [
            (c.id, c.nombre) for c in categorias_disponibles]

        # Puedes personalizar las etiquetas de campo y otros atributos si es necesario
        self.fields['q'].label = 'Buscar'
        self.fields['categorias'].label = 'Categorías'
        self.fields['fecha_publicacion'].label = 'Fecha de Publicación'
        self.fields['autor'].label = 'Autor'

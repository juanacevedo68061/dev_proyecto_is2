# En forms.py
from .models import Categoria  # Importa el modelo de categoría
from administracion.models import Categoria
from django import forms
from .models import Publicacion_solo_text

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion_solo_text
        fields = [
            'titulo', 'texto', 'categoria', 'palabras_clave',
            'vigencia', 'vigencia_unidad', 'vigencia_cantidad',
            'programar', 'programar_unidad', 'programar_cantidad',
            'suscriptores'
        ]

    UNIDADES_TIEMPO = (
        ('d', 'Días'),
        ('h', 'Horas'),
        ('m', 'Minutos'),
    )

    vigencia_unidad = forms.ChoiceField(choices=UNIDADES_TIEMPO, label='Unidad de Tiempo', required=False)
    programar_unidad = forms.ChoiceField(choices=UNIDADES_TIEMPO, label='Unidad de Tiempo', required=False)
    vigencia_cantidad = forms.IntegerField(label='Cantidad de Tiempo', required=False)
    programar_cantidad = forms.IntegerField(label='Cantidad de Tiempo', required=False)
    suscriptores = forms.BooleanField(label='Suscriptores', required=False)  # Campo añadido

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
        self.fields['vigencia'].widget.attrs.update(
            {'class': 'form-check-input', 'id': 'id_vigencia'})
        self.fields['programar'].widget.attrs.update(
            {'class': 'form-check-input', 'id': 'id_programar'})

        categorias = Categoria.objects.all()
        choices = [(categoria.pk, f"{categoria.nombre} ({'Moderada' if categoria.moderada else 'No moderada'})") for categoria in categorias]
        choices.insert(0, ('', '---------'))
        self.fields['categoria'].choices = choices

    def clean(self):
        cleaned_data = super().clean()
        vigencia = cleaned_data.get('vigencia')
        programar = cleaned_data.get('programar')

        if vigencia:
            vigencia_unidad = cleaned_data.get('vigencia_unidad')
            vigencia_cantidad = cleaned_data.get('vigencia_cantidad')
            if not vigencia_unidad or not vigencia_cantidad:
                self.add_error('vigencia_unidad', 'Este campo es requerido si selecciona vigencia.')
                self.add_error('vigencia_cantidad', 'Este campo es requerido si selecciona vigencia.')

        if programar:
            programar_unidad = cleaned_data.get('programar_unidad')
            programar_cantidad = cleaned_data.get('programar_cantidad')
            if not programar_unidad or not programar_cantidad:
                self.add_error('programar_unidad', 'Este campo es requerido si selecciona programar.')
                self.add_error('programar_cantidad', 'Este campo es requerido si selecciona programar.')


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

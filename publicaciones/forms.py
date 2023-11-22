from administracion.models import Categoria
from django import forms
from .models import Publicacion_solo_text
from froala_editor.widgets import FroalaEditor

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion_solo_text
        fields = [
            'titulo', 'texto', 'palabras_clave',
            'categoria_suscriptores',
            'categoria_no_suscriptores',
            'vigencia', 'vigencia_unidad', 'vigencia_cantidad',
            'programar', 'programar_unidad', 'programar_cantidad',
            
        ]

    UNIDADES_TIEMPO = [
        ('d', 'Días'),
        ('h', 'Horas'),
        ('m', 'Minutos'),
    ]
    texto = forms.CharField(widget=FroalaEditor)
    vigencia_unidad = forms.ChoiceField(choices=UNIDADES_TIEMPO, label='Unidad de Tiempo', required=False)
    programar_unidad = forms.ChoiceField(choices=UNIDADES_TIEMPO, label='Unidad de Tiempo', required=False)
    vigencia_cantidad = forms.IntegerField(label='Cantidad de Tiempo', required=False)
    programar_cantidad = forms.IntegerField(label='Cantidad de Tiempo', required=False)

    # Campos de selección de categorías
    categoria_suscriptores = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(suscriptores=True),
        label='Categoría para Suscriptores',
        required=False,
    )

    categoria_no_suscriptores = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(suscriptores=False),
        label='Categoría para No Suscriptores',
        required=False,
    )

    def __init__(self, kanban=True, tiene=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo'].widget.attrs.update({'class': 'form-control', 'id': 'id_titulo'})
        #self.fields['texto'].widget.attrs.update({'class': 'form-control', 'id': 'id_texto', 'rows': '4'})
        self.fields['palabras_clave'].widget.attrs.update({'class': 'form-control', 'id': 'id_palabras_clave'})
        self.fields['vigencia'].widget.attrs.update({'class': 'form-check-input', 'id': 'id_vigencia'})
        self.fields['programar'].widget.attrs.update({'class': 'form-check-input', 'id': 'id_programar'})
        self.fields['categoria_suscriptores'].widget.attrs.update({'class': 'form-control', 'id': 'id_categoria_suscriptores'})
        self.fields['categoria_no_suscriptores'].widget.attrs.update({'class': 'form-control', 'id': 'id_categoria_no_suscriptores'})
        self.fields['categoria_suscriptores'].choices = self.get_categoria_choices(True, kanban, tiene)
        self.fields['categoria_no_suscriptores'].choices = self.get_categoria_choices(False, kanban, tiene)
        if self.instance and self.instance.categoria:
            if self.instance.categoria.suscriptores:
                self.fields['categoria_suscriptores'].initial = self.instance.categoria
            else:
                self.fields['categoria_no_suscriptores'].initial = self.instance.categoria        
    def get_categoria_choices(self, suscriptores, kanban, tiene):
        if kanban:
            categorias = Categoria.objects.filter(suscriptores=suscriptores, moderada=True)
        else:
            if tiene:
                categorias = Categoria.objects.filter(suscriptores=suscriptores)
            else:
                categorias = Categoria.objects.filter(suscriptores=suscriptores, moderada=True)
        choices = [(categoria.pk, f"{categoria.nombre} ({'Moderada' if categoria.moderada else 'No Moderada'})") for categoria in categorias]
        choices.insert(0, ('', '---------'))
        return choices

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

    def __init__(self, anonimo, *args, **kwargs):
        super(BusquedaAvanzadaForm, self).__init__(*args, **kwargs)

        if not anonimo:
            categorias_disponibles = Categoria.objects.all()
        else:
            categorias_disponibles = Categoria.objects.filter(suscriptores = False)

        self.fields['categorias'].choices = [
            (c.id, c.nombre) for c in categorias_disponibles]

        self.fields['q'].label = 'Buscar'
        if categorias_disponibles:
            self.fields['categorias'].label = 'Categorías'
        else:
            del self.fields['categorias']
        self.fields['fecha_publicacion'].label = 'Fecha de Publicación'
        self.fields['autor'].label = 'Autor'
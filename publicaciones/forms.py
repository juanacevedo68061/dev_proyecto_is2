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
        ]

    texto = forms.CharField(widget=FroalaEditor)

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
        self.fields['palabras_clave'].widget.attrs.update({'class': 'form-control', 'id': 'id_palabras_clave'})
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
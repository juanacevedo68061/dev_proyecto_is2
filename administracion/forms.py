from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    """
    Formulario para crear y editar una categoría.

    Este formulario se utiliza para ingresar información sobre una categoría,
    incluyendo su nombre y estado de moderación.

    Campos:
    -------
    nombre : str
        Nombre de la categoría.
    moderada : bool
        Estado de moderación de la categoría (True para moderada, False para no moderada).

    """

    class Meta:
        model = Categoria
        fields = ['nombre', 'moderada']

    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)

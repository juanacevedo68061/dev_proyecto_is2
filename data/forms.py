from django import forms
from administracion.models import Categoria
from publicaciones.models import Publicacion_solo_text

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'moderada', 'suscriptores']

    def save_and_validate(self):
        if self.is_valid():
            categoria = self.save()  # Guardar la categoría en la base de datos
            print(f'Categoría "{categoria.nombre}" creada con éxito.')
            return categoria
        else:
            print('Error al crear la categoría.')
            return None

class PublicacionForm(forms.ModelForm):
    # Agregar el formulario de Categoría en línea
    categoria_form = CategoriaForm()

    class Meta:
        model = Publicacion_solo_text
        fields = [
            'titulo', 'texto', 'palabras_clave',
            'categoria_suscriptores',
            'categoria_no_suscriptores',
        ]

    def save_and_validate(self):
        if self.is_valid():
            categoria = self.categoria_form.save_and_validate()
            if categoria:
                publicacion = self.save()  # Guardar la publicación en la base de datos
                print(f'Publicación "{publicacion.titulo}" creada con éxito.')
                return publicacion
        print('Error al crear la publicación.')
        return None

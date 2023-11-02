from .forms import CategoriaForm, PublicacionForm


categoria_data = {
    'nombre': 'Nacional',
    'moderada': False,
    'suscriptores': False,
}

categoria_form = CategoriaForm(categoria_data)
categoria = categoria_form.save_and_validate()

if categoria:
    publicacion_data = {
        'titulo': '12 Websites You’ll Love As A Developer',
        'texto': 'PRIMERA PUBLICACION',
        'palabras_clave': 'primera',
        'categoria_suscriptores': categoria,
    }

    publicacion_form = PublicacionForm(publicacion_data)
    publicacion = publicacion_form.save_and_validate()

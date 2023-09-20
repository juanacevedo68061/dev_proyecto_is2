from django.shortcuts import render
from publicaciones.forms import BusquedaAvanzadaForm
from publicaciones.models import Publicacion_solo_text
from django.db.models import Q
from administracion.models import Categoria
from login.models import Usuario
from django.shortcuts import render

def principal(request):
    # Inicializa las publicaciones con la lista completa de publicaciones moderadas
    publicaciones = Publicacion_solo_text.objects.filter(
        categoria__moderada=False).order_by('-fecha_creacion')

    # Verificar si se ha enviado un formulario de búsqueda
    if 'q' in request.GET:
        # Si se hizo una búsqueda, llama a la función busqueda
        publicaciones, busqueda_avanzada_form = busqueda(request, publicaciones)
    else:
        busqueda_avanzada_form = BusquedaAvanzadaForm()

    # Obtener todas las categorías y usuarios del sistema
    categorias = Categoria.objects.all()
    usuarios = Usuario.objects.all()

    contexto = {
        'publicaciones': publicaciones,
        'busqueda_avanzada_form': busqueda_avanzada_form,
        'categorias': categorias,
        'usuarios': usuarios,
        'principal': True,
    }

    return render(request, 'cms/principal.html', contexto)

def busqueda(request, publicaciones):
    # Verificar si se ha enviado un formulario de búsqueda avanzada
    busqueda_avanzada_form = BusquedaAvanzadaForm(request.GET)

    # Si el formulario de búsqueda avanzada se ha enviado con datos, llama a busqueda_avanzada
    if busqueda_avanzada_form.is_valid() and busqueda_avanzada_form.has_changed():
        publicaciones = busqueda_avanzada(
            request, publicaciones, busqueda_avanzada_form)

    # Realiza el procesamiento adicional de las publicaciones (como hacer match) aquí
    query = request.GET.get('q')

    if query:
        # Hacer match con lo que ingresó el usuario en título, texto, palabras clave, etc.
        publicaciones = publicaciones.filter(
            Q(titulo__icontains=query) | Q(texto__icontains=query) | Q(palabras_clave__icontains=query))

    return publicaciones, busqueda_avanzada_form

def busqueda_avanzada(publicaciones, formulario):
    print("ENTRO A BUSQUEDA AVANZAAAAAAAAAAAAAAAAADA")
    # Procesa el formulario de búsqueda avanzada y realiza la búsqueda avanzada

    # Verificar los datos del formulario y filtrar las publicaciones según sea necesario
    categorias = formulario.cleaned_data.get('categorias')
    fecha_publicacion = formulario.cleaned_data.get('fecha_publicacion')
    autor = formulario.cleaned_data.get('autor')

    # Realizar búsqueda avanzada
    if categorias:
        publicaciones = publicaciones.filter(categoria__nombre__in=categorias)

    if fecha_publicacion:
        publicaciones = publicaciones.filter(
            fecha_creacion__date=fecha_publicacion)

    if autor:
        publicaciones = publicaciones.filter(autor__username=autor)

    return publicaciones

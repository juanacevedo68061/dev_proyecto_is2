from django.shortcuts import render
from publicaciones.forms import BusquedaAvanzadaForm
from publicaciones.models import Publicacion_solo_text
from django.db.models import Q
from administracion.models import Categoria
from login.models import Usuario
from django.shortcuts import render
from bs4 import BeautifulSoup
import re
import bleach

def principal(request):
    # Inicializa las publicaciones con la lista completa de publicaciones con estado publicado
    publicaciones = Publicacion_solo_text.objects.filter(
    estado='publicado',  # Filtrar por estado 'publicado'
    activo=True
    ).order_by('-fecha_creacion')


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

def buscador(request):    
    query = request.GET.get('q', '')  # Obtén el valor de búsqueda de la solicitud GET
    publicaciones = obtener_publicaciones(request)
    avanzada_form = BusquedaAvanzadaForm()

    if query:
        # Utilizamos expresiones regulares para buscar la consulta en el campo "texto"
        query = re.escape(query)  # Escapamos caracteres especiales en la consulta
        titulo = [publicacion for publicacion in publicaciones if re.search(query, publicacion.titulo, re.IGNORECASE)]
        texto = [publicacion for publicacion in publicaciones if re.search(query, bleach.clean(publicacion.texto, strip=True), re.IGNORECASE)]
        claves = [publicacion for publicacion in publicaciones if re.search(query, publicacion.palabras_clave, re.IGNORECASE)]
        
        # Concatenar las listas y eliminar duplicados
        resultados = titulo + texto + claves
        resultados = list(set(resultados))

        # Crear un QuerySet con los resultados
        publicaciones = Publicacion_solo_text.objects.filter(pk__in=[pub.pk for pub in resultados])
        
    contexto = {
        'publicaciones': publicaciones,
        'avanzada_form': avanzada_form
    }

    return render(request, 'cms/buscador.html', contexto)

def obtener_publicaciones(request):
    categorias = request.GET.getlist('categorias')
    fecha_publicacion = request.GET.get('fecha_publicacion')
    autor = request.GET.get('autor')
    print(categorias)
    print(fecha_publicacion)
    print(autor)


    publicaciones = Publicacion_solo_text.objects.filter(
        estado='publicado',
        activo=True
    ).order_by('-fecha_creacion')

    # Verificamos si los campos están vacíos o no
    if not any(categorias) and not fecha_publicacion and not autor:
        print("NO ENTRO")
    else:
        print("SI ENTRO")
        
        if categorias:
            publicaciones = publicaciones.filter(categoria__in=categorias)

        if fecha_publicacion:
            publicaciones = publicaciones.filter(fecha_publicacion=fecha_publicacion)

        if autor:
            publicaciones = [publicacion for publicacion in publicaciones if re.search(re.escape(autor), publicacion.autor.username, re.IGNORECASE)]

    return publicaciones

def busqueda(request, publicaciones):
    # Verificar si se ha enviado un formulario de búsqueda avanzada
    busqueda_avanzada_form = BusquedaAvanzadaForm(request.GET)

    # Si el formulario de búsqueda avanzada se ha enviado con datos, llama a busqueda_avanzada
    if busqueda_avanzada_form.has_changed():
        publicaciones = busqueda_avanzada(request, publicaciones, busqueda_avanzada_form)
    else:
        print("no es validooooooooooooooooooooooooo")
    # Realiza el procesamiento adicional de las publicaciones (como hacer match) aquí
    query = request.GET.get('q')

    if query:
        # Convertir la consulta a minúsculas
        query = query.lower()

        # Realizar las tres consultas y almacenar los resultados en listas
        publicaciones_titulo = list(publicaciones.filter(titulo__icontains=query))
        publicaciones_texto = [p for p in publicaciones if query in BeautifulSoup(p.texto, "html.parser").get_text().lower()]
        publicaciones_palabras_clave = list(publicaciones.filter(palabras_clave__icontains=query))

        # Combinar las listas en un solo conjunto de resultados único
        resultados = publicaciones_titulo + publicaciones_texto + publicaciones_palabras_clave

        # Eliminar duplicados
        resultados_unicos = list(set(resultados))

        # Convertir nuevamente a un QuerySet
        publicaciones = Publicacion_solo_text.objects.filter(pk__in=[publicacion.pk for publicacion in resultados_unicos])

    return publicaciones, busqueda_avanzada_form

def busqueda_avanzada(publicaciones, formulario):
    # Procesa el formulario de búsqueda avanzada y realiza la búsqueda avanzada
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    # Verificar los datos del formulario y filtrar las publicaciones según sea necesario
    categorias = formulario.cleaned_data.get('categorias')
    fecha_publicacion = formulario.cleaned_data.get('fecha_publicacion')
    autor = formulario.cleaned_data.get('autor')

    # Inicializar un conjunto de resultados que contiene todas las publicaciones
    resultados = publicaciones

    # Realizar búsqueda avanzada y combinar las consultas
    if categorias:
        resultados &= publicaciones.filter(categoria__nombre__in=categorias)

    if fecha_publicacion:
        resultados &= publicaciones.filter(fecha_creacion__date=fecha_publicacion)

    if autor:
        resultados &= publicaciones.filter(autor__username=autor)

    # Eliminar duplicados usando distinct()
    resultados = resultados.distinct()

    return resultados


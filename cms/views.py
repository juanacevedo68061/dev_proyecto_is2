from django.shortcuts import render
from publicaciones.forms import BusquedaAvanzadaForm
from publicaciones.models import Publicacion_solo_text
from administracion.models import Categoria
from django.shortcuts import render
import re
import bleach
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AnonymousUser
from django.db.models import Case, When, Value, IntegerField

def principal(request):

    """
    Vista principal que muestra las publicaciones. 
    También permite realizar búsquedas dentro de las publicaciones.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la plantilla 'cms/principal.html' con las publicaciones,
        formulario de búsqueda avanzada, categorías y usuarios.
    """
    anonimo = isinstance(request.user, AnonymousUser)
    query = request.GET.get('q')
    publicaciones_sin_orden = obtener_publicaciones(request, anonimo)
    publicaciones = ordenamiento(request, publicaciones_sin_orden)
    avanzada_form = BusquedaAvanzadaForm(anonimo)

    if not anonimo:
        categorias = Categoria.objects.all()
    else:
        categorias = Categoria.objects.filter(suscriptores=False)

    if query:
        # Utilizamos expresiones regulares para buscar la consulta en el campo "texto"
        query = re.escape(query)  # Escapamos caracteres especiales en la consulta
        titulo = [publicacion for publicacion in publicaciones if re.search(query, publicacion.titulo, re.IGNORECASE)]
        texto = [publicacion for publicacion in publicaciones if re.search(query, bleach.clean(publicacion.texto, strip=True), re.IGNORECASE)]
        claves = [publicacion for publicacion in publicaciones if re.search(query, publicacion.palabras_clave, re.IGNORECASE)]
        
        resultados = titulo + texto + claves
        resultados = list(set(resultados))

        publicaciones = Publicacion_solo_text.objects.filter(pk__in=[pub.pk for pub in resultados])
        
    contexto = {
        'publicaciones': publicaciones,
        'avanzada_form': avanzada_form,
        'categorias': categorias,
        'principal': True,
    }

    return render(request, 'cms/principal.html', contexto)

def obtener_publicaciones(request, anonimo):

    """
    Obtiene las publicaciones basadas en criterios de filtrado como categorías, fecha de publicación y autor.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        QuerySet: Retorna un conjunto de publicaciones filtradas.
    """

    categorias = request.GET.getlist('categorias')
    fecha_publicacion = request.GET.get('fecha_publicacion')
    autor = request.GET.get('autor')

    if not anonimo:
        publicaciones = Publicacion_solo_text.objects.filter(
            estado='publicado',
            activo=True
        ).order_by('-fecha_creacion')
    else:
        publicaciones = Publicacion_solo_text.objects.filter(
            estado='publicado',
            activo=True,
            categoria__suscriptores=False
        ).order_by('-fecha_creacion')
    
    if not (not any(categorias) and not fecha_publicacion and not autor):
        
        if categorias:
            publicaciones = publicaciones.filter(categoria__in=categorias)

        if fecha_publicacion:
            publicaciones = publicaciones.filter(fecha_publicacion__gte=fecha_publicacion)

        if autor:
            publicaciones = [publicacion for publicacion in publicaciones if re.search(re.escape(autor), publicacion.autor.username, re.IGNORECASE)]

    return publicaciones

def ordenamiento(request, publicaciones):
    anonimo = isinstance(request.user, AnonymousUser)
    destacadas = publicaciones.filter(destacado=True)
    favoritas = Publicacion_solo_text.objects.none()
    categorias_favoritas = Categoria.objects.none()
    if not anonimo:
        categorias_favoritas = Categoria.objects.filter(favorito_usuario=request.user)
        favoritas = publicaciones.filter(categoria__in=categorias_favoritas)

    restantes = publicaciones.exclude(destacado=True).exclude(categoria__in=categorias_favoritas)

    destacadas_list = list(destacadas)
    favoritas_list = list(favoritas)
    restantes_list = list(restantes)
    resultados = destacadas_list + favoritas_list + restantes_list

    ordenadas = Publicacion_solo_text.objects.filter(pk__in=[pub.pk for pub in resultados]).order_by(
    Case(*[When(pk=pub.pk, then=Value(index)) for index, pub in enumerate(resultados)], default=Value(len(resultados)), output_field=IntegerField()))

    return ordenadas

def publicaciones_categoria(request, categoria_id):

    """
    Muestra las publicaciones pertenecientes a una categoría específica.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        categoria_id (int): ID de la categoría de la cual se quieren obtener las publicaciones.

    Returns:
        HttpResponse: Renderiza la plantilla 'cms/principal.html' con las publicaciones de la categoría especificada.
    """

    categoria = get_object_or_404(Categoria, id=categoria_id)

    if not isinstance(request.user, AnonymousUser):
        categorias = Categoria.objects.all()
    else:
        categorias = Categoria.objects.filter(suscriptores=False)
        
    publicaciones = Publicacion_solo_text.objects.filter(categoria=categoria, activo=True, estado='publicado')
        
    return render(request, 'cms/principal.html', {'categorias': categorias, 'publicaciones': publicaciones, 'principal': True})

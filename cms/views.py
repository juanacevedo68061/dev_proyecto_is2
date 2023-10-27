from django.shortcuts import render
from publicaciones.forms import BusquedaAvanzadaForm
from publicaciones.models import Publicacion_solo_text
from administracion.models import Categoria
from login.models import Usuario
from django.shortcuts import render
import re
import bleach
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

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
    
    query = request.GET.get('q')
    publicaciones = obtener_publicaciones(request)
    avanzada_form = BusquedaAvanzadaForm()
    categorias = Categoria.objects.all()
    usuarios = Usuario.objects.all()

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
        'avanzada_form': avanzada_form,
        'categorias': categorias,
        'usuarios': usuarios,
        'principal': True,
    }

    return render(request, 'cms/principal.html', contexto)

def obtener_publicaciones(request):

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

    publicaciones = Publicacion_solo_text.objects.filter(
        estado='publicado',
        activo=True
    ).order_by('-fecha_creacion')

    # Verificamos si los campos están vacíos o no
    if not (not any(categorias) and not fecha_publicacion and not autor):
        
        if categorias:
            publicaciones = publicaciones.filter(categoria__in=categorias)

        if fecha_publicacion:
            publicaciones = publicaciones.filter(fecha_publicacion=fecha_publicacion)

        if autor:
            publicaciones = [publicacion for publicacion in publicaciones if re.search(re.escape(autor), publicacion.autor.username, re.IGNORECASE)]

    return publicaciones

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
    publicaciones = Publicacion_solo_text.objects.filter(categoria=categoria, activo=True, estado='publicado')
    categorias = Categoria.objects.all()
    redirect_url = None
    
    
    return render(request, 'cms/principal.html', {'categorias': categorias, 'publicaciones': publicaciones, 'principal': True, 'redirect_url': redirect_url })
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

@csrf_exempt #solucion temporal
def tinymce_upload(request):
    """
    Vista para manejar la carga de archivos a través de TinyMCE.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        JsonResponse: Devuelve la URL del archivo cargado o un error en caso de fallo.
    """
    
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_url = fs.url(filename)
        return JsonResponse({'location': file_url})
    return JsonResponse({'error': 'Failed to upload image.'})

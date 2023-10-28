from django.shortcuts import render
from cms.settings import GS_BUCKET_NAME
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
# from google.cloud import storage
# from my_storages.tinymce_storage import TinyMCELocalFileStorage
# import os

# def upload_to_gcloud(local_path, bucket_name, dest_path):
#     """Sube un archivo al bucket especificado en Google Cloud Storage."""
#     client = storage.Client()
#     bucket = client.get_bucket(bucket_name)
#     blob = bucket.blob(dest_path)
#     blob.upload_from_filename(local_path)
#     return blob.public_url

# @csrf_exempt
# def tinymce_upload(request):
#     if request.method == 'POST' and request.FILES['file']:
#         file = request.FILES['file']
        
#         # Guardar localmente
#         fs = TinyMCELocalFileStorage()
#         filename = fs.save(file.name, file)
#         local_file_url = fs.path(filename)

#         try:
#             # Subir a Google Cloud Storage
#             cloud_path = "publicados/" + file.name
#             cloud_url = upload_to_gcloud(local_file_url, GS_BUCKET_NAME, cloud_path)
            
#             # Opcional: Eliminar el archivo local después de subirlo a la nube
#             os.remove(local_file_url)
            
#             return JsonResponse({'location': cloud_url})
#         except Exception as e:
#             # En caso de error, es una buena práctica manejar la excepción y enviar una respuesta adecuada
#             return JsonResponse({'error': f'Failed to upload image to cloud. Error: {str(e)}'})
    
#     return JsonResponse({'error': 'Failed to upload image.'})
from django.core.files.storage import default_storage

@csrf_exempt
def tinymce_upload(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        
        # Guarda el archivo usando el sistema de almacenamiento predeterminado 
        filename = default_storage.save(file.name, file)
        
        # Obtiene la URL del archivo en GCS
        file_url = default_storage.url(filename)
        
        return JsonResponse({'location': file_url})
    return JsonResponse({'error': 'Failed to upload image.'})
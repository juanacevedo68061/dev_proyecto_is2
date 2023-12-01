

# Importar las clases y funciones necesarias para las pruebas
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from froala_editor import views

# Definir una clase para realizar pruebas de las URLs
class TestUrls(SimpleTestCase):

    # Prueba para verificar que la URL de carga de imágenes está correctamente enlazada a su vista
    def test_image_upload_url_resolves(self):
        # Obtener la URL usando su nombre
        url = reverse('froala_editor_image_upload')
        # Comprobar que la URL se resuelve a la función de vista correcta
        self.assertEquals(resolve(url).func, views.image_upload)

    # Prueba para la URL de carga de videos
    def test_video_upload_url_resolves(self):
        # Obtener la URL usando su nombre
        url = reverse('froala_editor_video_upload')
        # Comprobar que la URL se resuelve a la función de vista correspondiente
        self.assertEquals(resolve(url).func, views.video_upload)

    # Prueba para la URL del gestor de archivos
    def test_files_manager_upload_url_resolves(self):
        # Obtener la URL usando su nombre
        url = reverse('froala_editor_files_manager_upload')
        # Comprobar que la URL se resuelve a la función de vista adecuada
        self.assertEquals(resolve(url).func, views.files_manager_upload)

    # Prueba para la URL de carga de archivos
    def test_file_upload_url_resolves(self):
        # Obtener la URL usando su nombre
        url = reverse('froala_editor_file_upload')
        # Comprobar que la URL se resuelve a la función de vista asignada
        self.assertEquals(resolve(url).func, views.file_upload)
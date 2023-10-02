from django.test import SimpleTestCase
from django.urls import reverse, resolve
from canvan import views

class TestUrls(SimpleTestCase):

    def test_canvas_autor_url_resolves(self):
        url = reverse('canvan:canvas-autor')
        self.assertEquals(resolve(url).func, views.canvas_autor)

    def test_canvas_editor_url_resolves(self):
        url = reverse('canvan:canvas-editor')
        self.assertEquals(resolve(url).func, views.canvas_editor)

    def test_canvas_publicador_url_resolves(self):
        url = reverse('canvan:canvas-publicador')
        self.assertEquals(resolve(url).func, views.canvas_publicador)
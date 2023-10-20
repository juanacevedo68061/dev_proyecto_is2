from django.test import SimpleTestCase
from django.urls import reverse, resolve
from canvan import views

class TestUrls(SimpleTestCase):

    def test_canvas_autor_url_resolves(self):
        url = reverse('canvan:canvas-autor')
        self.assertEquals(resolve(url).func, views.canvas_autor)

   
   
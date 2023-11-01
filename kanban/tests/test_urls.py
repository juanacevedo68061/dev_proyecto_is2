from django.test import TestCase
from django.urls import reverse, resolve
from kanban import views

class KanvanURLsTestCase(TestCase):

    def test_kanban_url_resolves_to_kanban_view(self):
        url = reverse('kanvan:kanban')
        self.assertEqual(resolve(url).func, views.kanban)

    def test_actualizar_url_resolves_to_actualizar_view(self):
        url = reverse('kanvan:actualizar')
        self.assertEqual(resolve(url).func, views.actualizar)

    def test_motivo_url_resolves_to_motivo_view(self):
        url = reverse('kanvan:motivo')
        self.assertEqual(resolve(url).func, views.motivo)

    def test_historial_url_resolves_to_historial_view(self):
        url = reverse('kanvan:historial')
        self.assertEqual(resolve(url).func, views.historial)

from django.test import TestCase
from django.apps import apps
from login.apps import LoginConfig

class AppsTests(TestCase):
    def test_nombre_de_la_app(self):

        self.assertEqual(LoginConfig.name, 'login')

    def test_app_es_activa(self):
        app = apps.get_app_config('login')
        self.assertTrue(apps.is_installed('login'))
        self.assertTrue(app.name == 'login')

    def test_señales_importadas(self):
        try:
            from login import signals
        except ImportError:
            self.fail("No se pudieron importar las señales de la aplicación 'login'")

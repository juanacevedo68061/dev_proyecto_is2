from django.apps import apps
from django.test import TestCase
from kanban.apps import KanbanConfig

class KanbanConfigTest(TestCase):

    def test_apps_config(self):
        self.assertEqual(KanbanConfig.name, 'kanban')
        self.assertEqual(apps.get_app_config('kanban').name, 'kanban')

    def test_default_auto_field(self):
        self.assertEqual(KanbanConfig.default_auto_field, 'django.db.models.BigAutoField')

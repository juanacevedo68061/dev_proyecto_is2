from django.apps import AppConfig

class LoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # O el tipo de campo que estés usando
    name = 'login'

    def ready(self):
        import login.signals  # Importa las señales al iniciar la aplicación


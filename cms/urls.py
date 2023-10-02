from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... otras URLs ...
    path('', views.principal, name='principal'),
    path('tinymce/', include('tinymce.urls')),
    path('login/', include('login.urls', namespace='login')),
    path('administracion/', include('administracion.urls', namespace='administracion')),
    path('publicaciones/', include('publicaciones.urls', namespace='publicaciones')),
    path('canvan/', include('canvan.urls', namespace='canvan')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
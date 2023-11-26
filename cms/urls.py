from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.principal, name='principal'),
    path('froala_editor/', include('froala_editor.urls')),
    path('login/', include('login.urls', namespace='login')),
    path('administracion/', include('administracion.urls', namespace='administracion')),
    path('publicaciones/', include('publicaciones.urls', namespace='publicaciones')),
    path('kanban/', include('kanban.urls', namespace='kanban')),
    path('comentarios/', include('comentarios.urls', namespace='comentarios')),
    path('categoria/<int:categoria_id>/', views.publicaciones_categoria, name='publicaciones_categoria'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
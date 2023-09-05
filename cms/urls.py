from django.urls import path, include
from . import views

urlpatterns = [
    # ... otras URLs ...
    path('', views.principal, name='principal'),
    path('login/', include('login.urls', namespace='login')),
    path('administracion/', include('administracion.urls', namespace='administracion')),
    path('publicaciones/', include('publicaciones.urls', namespace='publicaciones')),
]

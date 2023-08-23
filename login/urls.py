from django.urls import path
from . import views

app_name = 'login'  

urlpatterns = [
    path('', views.inicio_sesion, name='inicio_sesion'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('activar-rol/', views.activar_rol, name='activar_rol'),
]


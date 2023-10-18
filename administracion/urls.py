from django.urls import path
from . import views

app_name = 'administracion'

urlpatterns = [
    path('', views.panel, name='panel'),
    path('categorias/', views.gestion_categorias, name='gestion_categorias'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('usuarios/', views.gestion_usuarios, name='gestion_usuarios'), 
    path('usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/asignar_roles/<int:usuario_id>/', views.asignar_roles_usuario, name='asignar_roles_usuario'),
    path('usuarios/eliminar_roles/<int:usuario_id>/', views.eliminar_roles_usuario, name='eliminar_roles_usuario'),
    path('usuarios/agregar_permisos/<int:usuario_id>/', views.agregar_permisos_roles_usuario, name='agregar_permisos_roles_usuario'),
    path('usuarios/eliminar_permisos/<int:usuario_id>/', views.eliminar_permisos_roles_usuario, name='eliminar_permisos_roles_usuario'),
]
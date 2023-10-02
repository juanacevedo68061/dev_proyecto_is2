from django.urls import path
from . import views

app_name = 'publicaciones'

urlpatterns = [
    path('crear/', views.crear_publicacion, name='crear_publicacion'),
    path('like/<int:pk>/', views.like_publicacion, name='like'),
    path('dislike/<int:pk>/', views.dislike_publicacion, name='dislike'),
    path('compartir/<int:pk>/', views.compartir_publicacion, name='compartir'),
    path('editar/<int:publicacion_id>/autor/', views.editar_publicacion_autor, name='editar_publicacion_autor'),
    path('eliminar/<int:publicacion_id>/', views.eliminar_publicacion_autor, name='eliminar-publicacion-autor'),
    path('editar/<int:publicacion_id>/editor/', views.editar_publicacion_editor, name='editar_publicacion_editor'),
    path('rechazar_editor/<int:publicacion_id>/', views.rechazar_editor, name='rechazar_editor'),
    path('ver/<int:publicacion_id>/', views.mostar_para_publicador, name='mostar_para_publicador'),
    path('mostrar/<int:publicacion_id>/', views.mostrar_publicacion, name='mostrar_publicacion'),
    path('rechazar_publicador/<int:publicacion_id>/', views.rechazar_publicador, name='rechazar_publicador'),
]



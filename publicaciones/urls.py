from django.urls import path
from . import views

app_name = 'publicaciones'

urlpatterns = [
    path('crear/', views.crear_publicacion, name='crear_publicacion'),
    path('like/<int:pk>/', views.like_publicacion, name='like'),
    path('dislike/<int:pk>/', views.dislike_publicacion, name='dislike'),
    path('compartir/<int:pk>/', views.compartir_publicacion, name='compartir'),
    # URLs para edición de publicación en el contexto de canvas-autor
    path('editar/<int:publicacion_id>/autor/', views.editar_publicacion_autor, name='editar_publicacion_autor'),
    # URLs para edición de publicación en el contexto de canvas-editor
    path('editar/<int:publicacion_id>/editor/', views.editar_publicacion_editor, name='editar_publicacion_editor'),
]



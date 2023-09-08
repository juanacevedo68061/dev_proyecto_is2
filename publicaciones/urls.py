from django.urls import path
from . import views

app_name = 'publicaciones'

urlpatterns = [
    path('crear/', views.crear_publicacion, name='crear_publicacion'),
    path('like/<int:pk>/', views.like_publicacion, name='like'),
    path('dislike/<int:pk>/', views.dislike_publicacion, name='dislike'),
    path('compartir/<int:pk>/', views.compartir_publicacion, name='compartir'),
]

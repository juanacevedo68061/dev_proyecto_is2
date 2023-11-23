from django.urls import path
from . import views

app_name = 'publicaciones'

urlpatterns = [
    path('crear/', views.crear_publicacion, name='crear_publicacion'),
    path('generar_qr/<uuid:publicacion_id>/', views.generar_qr, name='generar_qr'),
    path('editar/<uuid:publicacion_id>/autor/', views.editar_publicacion_autor, name='editar_publicacion_autor'),
    path('editar/<uuid:publicacion_id>/editor/', views.editar_publicacion_editor, name='editar_publicacion_editor'),
    path('ver/<uuid:publicacion_id>/', views.mostar_para_publicador, name='mostar_para_publicador'),
    path('mostrar/<uuid:publicacion_id>/', views.mostrar_publicacion, name='mostrar_publicacion'),
    path('compartidas/<uuid:publicacion_id>/', views.compartidas, name='compartidas'),
    path('like/<uuid:publicacion_id>/', views.like, name='like'),
    path('dislike/<uuid:publicacion_id>/', views.dislike, name='dislike'),
    path('track_view/<uuid:publicacion_id>/', views.track_view, name='track_view'),
    path('estado/<uuid:publicacion_id>/', views.estado, name='estado'),
    path('estatus/<uuid:publicacion_id>/', views.estatus, name='estatus'),
    path('calificar/<uuid:publicacion_id>/', views.calificar, name='calificar'),
    path('comments/post/', views.custom_post_comment, name='comments-post-comment'),
]



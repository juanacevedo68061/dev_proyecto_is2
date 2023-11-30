from django.urls import path
from . import views

app_name = 'comentarios'  

urlpatterns = [
    path('comentar/<uuid:publicacion_id>/', views.comentar, name='comentar'),
    path('responder/<int:comentario_id>/', views.responder, name='responder'),
    path('nuevo/<uuid:publicacion_id>/', views.nuevo, name='nuevo'),
    path('verificar/<uuid:publicacion_id>/', views.verificar, name='verificar'),
]


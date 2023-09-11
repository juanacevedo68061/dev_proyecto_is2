from django.urls import path
from . import views

app_name = 'canvan' 

urlpatterns = [
    path('canvas-autor/', views.canvas_autor, name='canvas-autor'),
    path('canvas-editor/', views.canvas_editor, name='canvas-editor'),
    path('canvas-publicador/', views.canvas_publicador, name='canvas-publicador'),
]

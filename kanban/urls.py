from django.urls import path
from . import views

app_name = 'kanvan' 

urlpatterns = [
    path('', views.kanban, name='kanban'),
]

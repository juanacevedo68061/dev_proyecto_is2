from django.urls import path, include
from . import views

urlpatterns = [
    # ... otras URLs ...
    path('', views.principal, name='principal'),
    path('login/', include('login.urls', namespace='login')),
]

from django.urls import path
from .views import contactar_vendedor

urlpatterns = [
    path('propiedad/<int:pk>/contactar/', contactar_vendedor, name='contactar_vendedor'),
]
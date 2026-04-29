from django.urls import path
from .views import contactar_vendedor, mensajes_recibidos

urlpatterns = [
    path('propiedad/<int:pk>/contactar/', contactar_vendedor, name='contactar_vendedor'),
    path('mensajes/', mensajes_recibidos, name='mensajes_recibidos'),
]
from django.urls import path
from .views import inicio, detalle_propiedad, crear_propiedad, mis_publicaciones, editar_propiedad, eliminar_propiedad

urlpatterns = [
    path('', inicio, name='inicio'),
    path('propiedad/<int:pk>/', detalle_propiedad, name='detalle_propiedad'),
    path('publicar/', crear_propiedad, name='crear_propiedad'),
    path('mis-publicaciones/', mis_publicaciones, name='mis_publicaciones'),
    path('propiedad/<int:pk>/editar/', editar_propiedad, name='editar_propiedad'),
    path('propiedad/<int:pk>/eliminar/', eliminar_propiedad, name='eliminar_propiedad'),
]
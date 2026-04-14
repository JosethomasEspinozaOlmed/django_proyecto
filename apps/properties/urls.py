from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='list'),
    path('propiedad/<int:pk>/', views.property_detail, name='detail'),
    path('publicar/', views.property_create, name='create'),
    path('propiedad/<int:pk>/editar/', views.property_edit, name='edit'),
    path('propiedad/<int:pk>/eliminar/', views.property_delete, name='delete'),
    path('mis-propiedades/', views.my_properties, name='my_properties'),
]

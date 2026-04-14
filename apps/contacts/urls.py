from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('<int:pk>/', views.contact_property, name='contact'),
]

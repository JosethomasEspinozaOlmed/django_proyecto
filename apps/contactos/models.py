from django.db import models
from apps.propiedades.models import Propiedad

class Contacto(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE, related_name='contactos')
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    mensaje = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.propiedad.titulo}"
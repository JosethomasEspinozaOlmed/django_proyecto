from django.contrib.auth.models import User
from django.db import models

from apps.propiedades.models import Propiedad


class Contacto(models.Model):

    propiedad = models.ForeignKey(
        Propiedad,
        on_delete=models.CASCADE,
        related_name="contactos",
    )

    comprador = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="mensajes_enviados",
        blank=True,
        null=True,
    )

    nombre = models.CharField(
        max_length=100,
    )

    contacto = models.CharField(
        max_length=100,
    )

    mensaje = models.TextField()

    creado = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-creado"]

    def __str__(self):
        return f"{self.nombre} - " f"{self.propiedad.titulo}"

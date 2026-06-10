from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    ROL_CHOICES = (
        ('comprador', 'Comprador'),
        ('vendedor', 'Vendedor'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"
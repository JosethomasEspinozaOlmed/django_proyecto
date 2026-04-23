from django.db import models
from django.contrib.auth.models import User

class Propiedad(models.Model):
    TIPO_CHOICES = (
        ('casa', 'Casa'),
        ('depto', 'Departamento'),
        ('terreno', 'Terreno'),
    )

    ESTADO_CHOICES = (
        ('activa', 'Activa'),
        ('pausada', 'Pausada'),
    )

    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='propiedades')
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    ciudad = models.CharField(max_length=100)
    barrio = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    superficie = models.PositiveIntegerField()
    dormitorios = models.PositiveIntegerField(default=0)
    banos = models.PositiveIntegerField(default=0)
    cochera = models.BooleanField(default=False)
    descripcion = models.TextField()
    foto_principal = models.ImageField(upload_to='propiedades/')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activa')
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
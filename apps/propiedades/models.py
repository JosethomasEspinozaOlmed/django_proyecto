from decimal import Decimal 
 
from django.contrib.auth.models import User 
from django.core.validators import MinValueValidator 
from django.db import models 
 
class Propiedad(models.Model): 
 
    TIPO_CHOICES = ( 
        ("casa", "Casa"), 
        ("depto", "Departamento"), 
        ("terreno", "Terreno"), 
    ) 
 
    ESTADO_CHOICES = ( 
        ("activa", "Activa"), 
        ("pausada", "Pausada"), 
    ) 
 
    MONEDA_CHOICES = ( 
        ("USD", "Dólar (USD)"), 
        ("PYG", "Guaraníes (PYG)"), 
    ) 
 
    DEPARTAMENTO_CHOICES = ( 
        ("Asunción", "Asunción"), 
        ("Central", "Central"), 
        ("Alto Paraguay", "Alto Paraguay"), 
        ("Alto Paraná", "Alto Paraná"), 
        ("Amambay", "Amambay"), 
        ("Boquerón", "Boquerón"), 
        ("Caaguazú", "Caaguazú"), 
        ("Caazapá", "Caazapá"), 
        ("Canindeyú", "Canindeyú"), 
        ("Concepción", "Concepción"), 
        ("Cordillera", "Cordillera"), 
        ("Guairá", "Guairá"), 
        ("Itapúa", "Itapúa"), 
        ("Misiones", "Misiones"), 
        ("Ñeembucú", "Ñeembucú"), 
        ("Paraguarí", "Paraguarí"), 
        ("Presidente Hayes", "Presidente Hayes"), 
        ("San Pedro", "San Pedro"), 
    ) 
 
    vendedor = models.ForeignKey( 
        User, 
        on_delete=models.CASCADE, 
        related_name="propiedades", 
    ) 
 
    titulo = models.CharField( 
        max_length=200, 
    ) 
 
    tipo = models.CharField( 
        max_length=20, 
        choices=TIPO_CHOICES, 
    ) 
 
    precio = models.DecimalField( 
        max_digits=12, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal("1"))], 
    ) 
 
    moneda = models.CharField( 
        max_length=3, 
        choices=MONEDA_CHOICES, 
        default="USD", 
    ) 
 
    departamento = models.CharField( 
        max_length=50, 
        choices=DEPARTAMENTO_CHOICES, 
        blank=True, 
        null=True, 
    ) 
 
    ciudad = models.CharField( 
        max_length=100, 
    ) 
 
    barrio = models.CharField( 
        max_length=100, 
        blank=True, 
        null=True, 
    ) 
 
    direccion = models.CharField( 
        max_length=255, 
        blank=True, 
        null=True, 
    ) 
 
    superficie = 
models.PositiveIntegerField(validators=[MinValueValidator(1)]) 
 
    dormitorios = models.PositiveIntegerField( 
        default=0, 
    ) 
 
    banos = models.PositiveIntegerField( 
        default=0, 
    ) 
 
    cochera = models.BooleanField( 
        default=False, 
    ) 
 
    descripcion = models.TextField() 
 
    foto_principal = models.ImageField( 
        upload_to="propiedades/", 
    ) 
 
    estado = models.CharField( 
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default="activa", 
    ) 
 
    creado = models.DateTimeField( 
        auto_now_add=True, 
    ) 
 
    ubicacion = models.URLField( 
        max_length=500, 
        blank=True, 
        null=True, 
    ) 
 
    latitud = models.DecimalField( 
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True, 
    ) 
 
    longitud = models.DecimalField( 
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True, 
    ) 
 
    class Meta: 
        ordering = ["-creado"] 
 
    def __str__(self): 
        return self.titulo 
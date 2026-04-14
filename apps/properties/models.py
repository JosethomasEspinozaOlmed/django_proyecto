from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image
import os


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name='Ciudad')
    department = models.CharField(max_length=100, verbose_name='Departamento', blank=True)

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, {self.department}' if self.department else self.name


class Property(models.Model):
    TYPE_CHOICES = [
        ('house', 'Casa'),
        ('apartment', 'Departamento'),
        ('land', 'Terreno'),
        ('commercial', 'Local comercial'),
    ]
    STATUS_CHOICES = [
        ('active', 'Activa'),
        ('paused', 'Pausada'),
        ('sold', 'Vendida'),
    ]

    seller = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='properties', verbose_name='Vendedor'
    )
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    property_type = models.CharField(
        max_length=15, choices=TYPE_CHOICES,
        default='house', verbose_name='Tipo'
    )
    price = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Precio (USD)'
    )
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True,
        related_name='properties', verbose_name='Ciudad'
    )
    address = models.CharField(max_length=300, verbose_name='Dirección', blank=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        null=True, blank=True, verbose_name='Latitud'
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        null=True, blank=True, verbose_name='Longitud'
    )
    bedrooms = models.PositiveIntegerField(default=0, verbose_name='Dormitorios')
    bathrooms = models.PositiveIntegerField(default=0, verbose_name='Baños')
    area_m2 = models.DecimalField(
        max_digits=8, decimal_places=2,
        null=True, blank=True, verbose_name='Superficie (m²)'
    )
    has_garage = models.BooleanField(default=False, verbose_name='Cochera')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES,
        default='active', verbose_name='Estado'
    )
    views_count = models.PositiveIntegerField(default=0, verbose_name='Visitas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Propiedad'
        verbose_name_plural = 'Propiedades'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('properties:detail', kwargs={'pk': self.pk})

    @property
    def cover_photo(self):
        photo = self.photos.filter(is_cover=True).first()
        if not photo:
            photo = self.photos.first()
        return photo

    @property
    def price_formatted(self):
        return f'${self.price:,.0f}'


class PropertyPhoto(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE,
        related_name='photos', verbose_name='Propiedad'
    )
    image = models.ImageField(upload_to='properties/', verbose_name='Imagen')
    thumbnail = models.ImageField(
        upload_to='properties/thumbs/', blank=True, null=True
    )
    is_cover = models.BooleanField(default=False, verbose_name='Foto principal')
    order = models.PositiveIntegerField(default=0, verbose_name='Orden')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'
        ordering = ['-is_cover', 'order']

    def __str__(self):
        return f'Foto de {self.property.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._resize_image()
        self._generate_thumbnail()

    def _resize_image(self):
        if self.image:
            img_path = self.image.path
            if os.path.exists(img_path):
                img = Image.open(img_path)
                max_size = (1200, 900)
                img.thumbnail(max_size, Image.LANCZOS)
                img.save(img_path, quality=85, optimize=True)

    def _generate_thumbnail(self):
        if self.image and not self.thumbnail:
            from django.core.files.base import ContentFile
            from io import BytesIO
            img = Image.open(self.image.path)
            img.thumbnail((400, 300), Image.LANCZOS)
            thumb_io = BytesIO()
            fmt = 'JPEG' if self.image.name.lower().endswith(('jpg', 'jpeg')) else 'PNG'
            img.save(thumb_io, format=fmt, quality=80)
            thumb_name = f'thumb_{os.path.basename(self.image.name)}'
            self.thumbnail.save(thumb_name, ContentFile(thumb_io.getvalue()), save=True)

from django.db import models
from apps.properties.models import Property


class ContactMessage(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE,
        related_name='messages', verbose_name='Propiedad'
    )
    sender_name = models.CharField(max_length=150, verbose_name='Nombre')
    sender_email = models.EmailField(verbose_name='Email')
    sender_phone = models.CharField(max_length=25, blank=True, verbose_name='Teléfono / WhatsApp')
    message = models.TextField(verbose_name='Mensaje')
    is_read = models.BooleanField(default=False, verbose_name='Leído')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mensaje de contacto'
        verbose_name_plural = 'Mensajes de contacto'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.sender_name} → {self.property.title}'

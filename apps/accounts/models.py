from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('buyer', 'Comprador'),
        ('seller', 'Vendedor'),
        ('admin', 'Administrador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Teléfono / WhatsApp')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, verbose_name='Descripción')
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuarios'

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.email} ({self.get_role_display()})'

    @property
    def is_seller(self):
        return self.role == 'seller'

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

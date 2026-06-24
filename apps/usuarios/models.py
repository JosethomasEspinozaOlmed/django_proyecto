from django.contrib.auth.models import User
from django.db import models


class Perfil(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    telefono = models.CharField(max_length=20)
    es_comprador = models.BooleanField(default=True)
    es_vendedor = models.BooleanField(default=True)

    @property
    def roles_display(self):
        roles = []

        if self.es_comprador:
            roles.append("Comprador")

        if self.es_vendedor:
            roles.append("Vendedor")

        return " y ".join(roles) or "Sin rol"

    def __str__(self):
        return f"{self.user.username} - {self.roles_display}"

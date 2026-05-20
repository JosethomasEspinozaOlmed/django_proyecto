import os
import django
from decimal import Decimal
from django.contrib.auth.models import User
from apps.usuarios.models import Perfil
from apps.propiedades.models import Propiedad

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


def create_test_user():
    u, created = User.objects.get_or_create(
        username="tester_autotest", defaults={"email": "test@example.com"}
    )
    if created:
        u.set_password("test")
        u.save()
    p, pc = Perfil.objects.get_or_create(user=u, defaults={"rol": "vendedor"})
    if p.rol != "vendedor":
        p.rol = "vendedor"
        p.save()
    return u


def create_test_prop(user):
    prop, created = Propiedad.objects.get_or_create(
        titulo="Propiedad de prueba automatizada",
        defaults={
            "vendedor": user,
            "tipo": "casa",
            "precio": Decimal("1200000"),
            "moneda": "PYG",
            "departamento": "Central",
            "ciudad": "Luque",
            "superficie": 120,
            "dormitorios": 3,
            "banos": 2,
            "descripcion": "Creada por script de prueba",
            "foto_principal": "propiedades/test.jpg",
        },
    )
    return prop


if __name__ == "__main__":
    user = create_test_user()
    prop = create_test_prop(user)
    print("Usuario:", user.username, "Perfil rol:", user.perfil.rol)
    print(
        "Propiedad creada/id:",
        prop.id,
        prop.titulo,
        prop.precio,
        prop.moneda,
        prop.departamento,
        prop.ciudad,
    )

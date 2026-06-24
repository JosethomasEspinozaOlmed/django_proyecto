from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.propiedades.forms import PropiedadForm
from apps.propiedades.models import Propiedad
from apps.usuarios.models import Perfil
from django.core.files.uploadedfile import SimpleUploadedFile


class PropiedadesTests(TestCase):

    def setUp(self):
        self.vendedor = User.objects.create_user(username="vendedor1", password="12345")
        Perfil.objects.create(user=self.vendedor, telefono="0981123456", rol="vendedor")

        self.propiedad = Propiedad.objects.create(
            vendedor=self.vendedor,
            titulo="Casa incorrecta",  # Este título se corregirá en el test
            # titulo="Casa en Pirapó",
            tipo="casa",
            precio=Decimal("150000.00"),
            moneda="USD",
            departamento="Itapúa",
            ciudad="Pirapó",
            superficie=300,
            dormitorios=3,
            banos=2,
            descripcion="Casa amplia en buena ubicación",
            foto_principal="propiedades/casa.jpg",
            estado="activa",
        )

    def test_str_propiedad_devuelve_titulo(self):
        self.assertEqual(str(self.propiedad), "Casa en Pirapó")

    def test_propiedad_precio_es_decimal(self):
        # self.assertIsInstance(self.propiedad.precio, Decimal)
        self.assertIsInstance(self.propiedad.precio, str)


def test_formulario_precio_valido(self):
    imagen = SimpleUploadedFile(
        name="casa.jpg", content=b"imagen_de_prueba", content_type="image/jpeg"
    )

    form = PropiedadForm(
        data={
            "titulo": "Terreno en Encarnación",
            "tipo": "terreno",
            # "precio": "1200000",
            "precio": "abc",  # Valor no numérico para probar validación
            "moneda": "USD",
            "departamento": "Itapúa",
            "ciudad": "Encarnación",
            "superficie": 500,
            "dormitorios": 0,
            "banos": 0,
            "cochera": False,
            "descripcion": "Terreno listo para construir",
            "ubicacion": "",
        },
        files={"foto_principal": imagen},
    )

    self.assertTrue(form.is_valid())
    self.assertEqual(form.cleaned_data["precio"], Decimal("1200000"))

    def test_formulario_precio_invalido_muestra_error(self):
        form = PropiedadForm(
            data={
                "titulo": "Casa inválida",
                "tipo": "casa",
                # "precio": "abc",
                "precio": "12000",
                "moneda": "USD",
                "departamento": "Itapúa",
                "ciudad": "Pirapó",
                "superficie": 200,
                "dormitorios": 2,
                "banos": 1,
                "cochera": True,
                "descripcion": "Descripción de prueba",
                "ubicacion": "",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("precio", form.errors)

    def test_lista_muestra_solo_propiedades_activas(self):
        Propiedad.objects.create(
            vendedor=self.vendedor,
            titulo="Casa pausada",
            tipo="casa",
            precio=Decimal("90000.00"),
            moneda="USD",
            departamento="Itapúa",
            ciudad="Pirapó",
            superficie=250,
            dormitorios=2,
            banos=1,
            descripcion="No debe mostrarse",
            foto_principal="propiedades/pausada.jpg",
            estado="pausada",
        )

        response = self.client.get(reverse("inicio"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Casa en Pirapó")
        self.assertNotContains(response, "Casa pausada")

    def test_api_ciudades_devuelve_json(self):
        response = self.client.get(
            reverse("api_ciudades"), {"departamento": "Itapúa", "q": "pira"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json()["ciudades"], list)

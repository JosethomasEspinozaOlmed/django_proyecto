import base64
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from apps.propiedades.forms import PropiedadForm
from apps.propiedades.models import Propiedad
from apps.usuarios.models import Perfil


class PropiedadesTests(TestCase):

    def setUp(self):
        self.vendedor = User.objects.create_user(
            username="vendedor1",
            password="12345",
        )

        Perfil.objects.create(
            user=self.vendedor,
            telefono="0981123456",
            es_comprador=False,
            es_vendedor=True,
        )

        self.propiedad = Propiedad.objects.create(
            vendedor=self.vendedor,
            titulo="Casa en Pirapó",
            tipo="casa",
            precio=Decimal("150000.00"),
            moneda="USD",
            departamento="Itapúa",
            ciudad="Pirapó",
            superficie=300,
            dormitorios=3,
            banos=2,
            descripcion="Casa amplia ubicada en una zona tranquila de Pirapó.",
            foto_principal="propiedades/casa.jpg",
            estado="activa",
            latitud=Decimal("-26.860000"),
            longitud=Decimal("-55.540000"),
        )

    def crear_imagen(self):
        imagen_png = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwC"
            "AAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        )

        return SimpleUploadedFile(
            name="casa.png",
            content=imagen_png,
            content_type="image/png",
        )

    def test_str_propiedad_devuelve_titulo(self):
        self.assertEqual(
            str(self.propiedad),
            "Casa en Pirapó",
        )

    def test_propiedad_precio_es_decimal(self):
        self.assertIsInstance(
            self.propiedad.precio,
            Decimal,
        )

    def test_formulario_precio_valido(self):
        formulario = PropiedadForm(
            data={
                "titulo": "Terreno en Encarnación",
                "tipo": "terreno",
                "precio": "1.200.000",
                "moneda": "USD",
                "departamento": "Itapúa",
                "ciudad": "Encarnación",
                "barrio": "",
                "direccion": "",
                "superficie": 500,
                "dormitorios": 0,
                "banos": 0,
                "cochera": False,
                "descripcion": (
                    "Terreno amplio y preparado para construir una vivienda."
                ),
                "latitud": "-27.330560",
                "longitud": "-55.866670",
            },
            files={
                "foto_principal": self.crear_imagen(),
            },
        )

        self.assertTrue(
            formulario.is_valid(),
            formulario.errors,
        )

        self.assertEqual(
            formulario.cleaned_data["precio"],
            Decimal("1200000"),
        )

    def test_formulario_precio_invalido_muestra_error(self):
        formulario = PropiedadForm(
            data={
                "titulo": "Casa inválida",
                "tipo": "casa",
                "precio": "abc",
                "moneda": "USD",
                "departamento": "Itapúa",
                "ciudad": "Pirapó",
                "superficie": 200,
                "dormitorios": 2,
                "banos": 1,
                "cochera": True,
                "descripcion": (
                    "Descripción suficientemente extensa para la propiedad."
                ),
                "latitud": "-26.860000",
                "longitud": "-55.540000",
            },
            files={
                "foto_principal": self.crear_imagen(),
            },
        )

        self.assertFalse(formulario.is_valid())
        self.assertIn("precio", formulario.errors)

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
            descripcion="Esta propiedad pausada no debe mostrarse en el inicio.",
            foto_principal="propiedades/pausada.jpg",
            estado="pausada",
        )

        respuesta = self.client.get(reverse("inicio"))

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Casa en Pirapó")
        self.assertNotContains(respuesta, "Casa pausada")

    def test_api_ciudades_devuelve_json(self):
        respuesta = self.client.get(
            reverse("api_ciudades"),
            {
                "departamento": "Itapúa",
            },
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertIsInstance(
            respuesta.json()["ciudades"],
            list,
        )
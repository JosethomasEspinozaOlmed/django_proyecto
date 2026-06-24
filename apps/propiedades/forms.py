import re

from decimal import Decimal, InvalidOperation
from urllib.parse import urlparse

from django import forms

from .models import Propiedad


class PropiedadForm(forms.ModelForm):

    departamento = forms.ChoiceField(
        label="Departamento",
        choices=Propiedad.DEPARTAMENTO_CHOICES,
        required=True,
        widget=forms.Select(
            attrs={
                "class": ("form-select departamento-select"),
            }
        ),
    )

    precio = forms.CharField(
        label="Precio",
        widget=forms.TextInput(
            attrs={
                "class": "form-control precio-input",
                "placeholder": "Ej: 350.000.000",
                "inputmode": "decimal",
            }
        ),
    )

    class Meta:
        model = Propiedad

        exclude = [
            "vendedor",
            "estado",
            "creado",
        ]

        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": ("Ej: Casa familiar con patio"),
                    "maxlength": 200,
                }
            ),
            "tipo": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "moneda": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "ciudad": forms.TextInput(
                attrs={
                    "class": ("form-control ciudad-input"),
                    "placeholder": "Ej: Encarnación",
                    "list": "ciudades-list",
                    "autocomplete": "off",
                }
            ),
            "barrio": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: San Roque",
                }
            ),
            "direccion": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": ("Ej: Av. principal casi calle 2"),
                }
            ),
            "ubicacion": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": ("https://maps.app.goo.gl/..."),
                }
            ),
            "superficie": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: 180",
                    "min": 1,
                    "max": 10000000,
                }
            ),
            "dormitorios": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 100,
                }
            ),
            "banos": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 100,
                }
            ),
            "cochera": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": (
                        "Contá los aspectos principales " "de la propiedad..."
                    ),
                    "rows": 5,
                    "maxlength": 3000,
                }
            ),
            "foto_principal": (
                forms.ClearableFileInput(
                    attrs={
                        "class": "form-control",
                        "accept": ("image/jpeg," "image/png," "image/webp"),
                    }
                )
            ),
        }

        labels = {
            "titulo": "Título de la publicación",
            "tipo": "Tipo de propiedad",
            "moneda": "Moneda",
            "departamento": "Departamento",
            "ciudad": "Ciudad",
            "barrio": "Barrio",
            "direccion": "Dirección o referencia",
            "superficie": "Superficie (m²)",
            "dormitorios": "Dormitorios",
            "banos": "Baños",
            "cochera": "Tiene cochera",
            "descripcion": "Descripción",
            "foto_principal": "Foto principal",
            "ubicacion": "Enlace de Google Maps",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["foto_principal"].required = False

            self.initial["precio"] = self._format_initial_price(self.instance.precio)

        for name, field in self.fields.items():
            if name != "cochera":
                field.widget.attrs.setdefault(
                    "aria-describedby",
                    f"help-{name}",
                )

    @staticmethod
    def _format_initial_price(value):
        if value is None:
            return ""

        return format(value, "f").rstrip("0").rstrip(".")

    @staticmethod
    def _normalize_decimal(raw):
        texto = str(raw).strip().replace(" ", "")

        if not texto or not re.fullmatch(
            r"[0-9.,]+",
            texto,
        ):
            raise InvalidOperation

        if "," in texto and "." in texto:
            ultima_coma = texto.rfind(",")
            ultimo_punto = texto.rfind(".")

            if ultima_coma > ultimo_punto:
                texto = texto.replace(".", "").replace(",", ".")
            else:
                texto = texto.replace(",", "")

        elif texto.count(",") > 1:
            texto = texto.replace(",", "")

        elif texto.count(".") > 1:
            texto = texto.replace(".", "")

        elif "," in texto:
            entero, decimal = texto.split(",")

            if 1 <= len(decimal) <= 2:
                texto = f"{entero}.{decimal}"
            else:
                texto = f"{entero}{decimal}"

        elif "." in texto:
            entero, decimal = texto.split(".")

            if len(decimal) == 3:
                texto = f"{entero}{decimal}"

        return Decimal(texto)

    def clean_titulo(self):
        titulo = " ".join(self.cleaned_data["titulo"].split())

        if len(titulo) < 8:
            raise forms.ValidationError(
                "El título debe tener al menos " "8 caracteres."
            )

        if not re.search(
            r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]",
            titulo,
        ):
            raise forms.ValidationError("El título debe contener palabras.")

        return titulo

    def clean_precio(self):
        try:
            precio = self._normalize_decimal(
                self.cleaned_data.get(
                    "precio",
                    "",
                )
            )

        except (InvalidOperation, ValueError):
            raise forms.ValidationError("Ingresá un precio válido.")

        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor que cero.")

        if precio >= Decimal("10000000000"):
            raise forms.ValidationError("El precio supera el límite permitido.")

        if abs(precio.as_tuple().exponent) > 2:
            raise forms.ValidationError(
                "El precio admite como máximo " "dos decimales."
            )

        return precio

    def clean_ciudad(self):
        ciudad = " ".join(self.cleaned_data["ciudad"].split())

        if len(ciudad) < 2 or not re.search(
            r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]",
            ciudad,
        ):
            raise forms.ValidationError("Ingresá una ciudad válida.")

        return ciudad.title()

    def clean_barrio(self):
        barrio = self.cleaned_data.get("barrio") or ""

        return " ".join(barrio.split())

    def clean_direccion(self):
        direccion = self.cleaned_data.get("direccion") or ""

        return " ".join(direccion.split())

    def clean_descripcion(self):
        descripcion = " ".join(self.cleaned_data["descripcion"].split())

        if len(descripcion) < 30:
            raise forms.ValidationError(
                "La descripción debe tener " "al menos 30 caracteres."
            )

        return descripcion

    def clean_ubicacion(self):
        url = self.cleaned_data.get("ubicacion") or ""

        if not url:
            return ""

        host = urlparse(url).netloc.lower()

        sitios_validos = (
            "google.com",
            "google.com.py",
            "maps.app.goo.gl",
            "goo.gl",
        )

        es_valido = any(
            host == sitio or host.endswith(f".{sitio}") for sitio in sitios_validos
        )

        if not es_valido:
            raise forms.ValidationError("Pegá un enlace válido " "de Google Maps.")

        return url

    def clean_foto_principal(self):
        imagen = self.cleaned_data.get("foto_principal")

        if not imagen:
            if not self.instance.pk:
                raise forms.ValidationError("Seleccioná una foto principal.")

            return imagen

        limite = 5 * 1024 * 1024

        if imagen.size > limite:
            raise forms.ValidationError("La imagen no puede superar " "los 5 MB.")

        tipo_archivo = getattr(
            imagen,
            "content_type",
            "",
        )

        permitidos = {
            "image/jpeg",
            "image/png",
            "image/webp",
        }

        if tipo_archivo and tipo_archivo not in permitidos:
            raise forms.ValidationError("Usá una imagen JPG, PNG o WEBP.")

        return imagen

    def clean(self):
        datos = super().clean()

        tipo = datos.get("tipo")
        dormitorios = datos.get("dormitorios")
        banos = datos.get("banos")

        if dormitorios is not None and dormitorios > 100:
            self.add_error(
                "dormitorios",
                "Ingresá una cantidad válida.",
            )

        if banos is not None and banos > 100:
            self.add_error(
                "banos",
                "Ingresá una cantidad válida.",
            )

        if tipo == "terreno":
            datos["dormitorios"] = 0
            datos["banos"] = 0
            datos["cochera"] = False

        return datos

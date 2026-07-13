import re

from decimal import Decimal, InvalidOperation

from django import forms

from .data import get_ciudades_for_departamento
from .models import Propiedad


class PropiedadForm(forms.ModelForm):

    precio = forms.CharField(
        label="Precio",
        widget=forms.TextInput(
            attrs={
                "class": "form-control precio-input",
                "placeholder": "Ej: 350.000.000",
                "inputmode": "numeric",
                "autocomplete": "off",
            }
        ),
    )

    departamento = forms.ChoiceField(
        label="Departamento",
        choices=(
            ("", "Seleccioná un departamento"),
        ) + Propiedad.DEPARTAMENTO_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select departamento-select",
            }
        ),
    )

    ciudad = forms.ChoiceField(
        label="Ciudad",
        choices=(
            ("", "Primero elegí un departamento"),
        ),
        widget=forms.Select(
            attrs={
                "class": "form-select ciudad-select",
            }
        ),
    )

    class Meta:
        model = Propiedad

        fields = [
            "titulo",
            "tipo",
            "precio",
            "moneda",
            "departamento",
            "ciudad",
            "barrio",
            "direccion",
            "superficie",
            "dormitorios",
            "banos",
            "cochera",
            "descripcion",
            "foto_principal",
            "latitud",
            "longitud",
        ]

        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: Casa familiar con amplio patio",
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

            "barrio": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: San Roque",
                }
            ),

            "direccion": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: Avenida principal casi calle 2",
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
                        "Describí las características principales "
                        "de la propiedad..."
                    ),
                    "rows": 5,
                    "maxlength": 3000,
                }
            ),

            "foto_principal": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/jpeg,image/png,image/webp",
                }
            ),

            "latitud": forms.HiddenInput(),

            "longitud": forms.HiddenInput(),
        }

        labels = {
            "titulo": "Título de la publicación",
            "tipo": "Tipo de propiedad",
            "moneda": "Moneda",
            "departamento": "Departamento",
            "ciudad": "Ciudad",
            "barrio": "Barrio",
            "direccion": "Dirección o referencia",
            "superficie": "Superficie en m²",
            "dormitorios": "Dormitorios",
            "banos": "Baños",
            "cochera": "Tiene cochera",
            "descripcion": "Descripción",
            "foto_principal": "Foto principal",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        departamento = ""

        if self.is_bound:
            departamento = self.data.get(
                "departamento",
                "",
            )

        elif self.instance and self.instance.pk:
            departamento = (
                self.instance.departamento
                or ""
            )

        ciudades = get_ciudades_for_departamento(
            departamento
        )

        self.fields["ciudad"].choices = [
            ("", "Seleccioná una ciudad"),
            *[
                (ciudad, ciudad)
                for ciudad in ciudades
            ],
        ]

        if self.instance and self.instance.pk:
            self.fields[
                "foto_principal"
            ].required = False

            if (
                not self.is_bound
                and self.instance.precio is not None
            ):
                precio = int(
                    self.instance.precio
                )

                self.initial["precio"] = (
                    f"{precio:,}".replace(",", ".")
                )

    def clean_titulo(self):
        titulo = " ".join(
            self.cleaned_data["titulo"].split()
        )

        if len(titulo) < 8:
            raise forms.ValidationError(
                "El título debe tener al menos 8 caracteres."
            )

        return titulo

    def clean_precio(self):
        valor = str(
            self.cleaned_data.get(
                "precio",
                "",
            )
        ).strip()

        if not valor:
            raise forms.ValidationError(
                "Ingresá el precio de la propiedad."
            )

        if "." in valor:
            formato_valido = re.fullmatch(
                r"\d{1,3}(?:\.\d{3})+",
                valor,
            )

            if not formato_valido:
                raise forms.ValidationError(
                    "Ingresá un precio válido. "
                    "Ejemplo: 350.000.000"
                )

        numero_limpio = valor.replace(
            ".",
            "",
        )

        if not numero_limpio.isdigit():
            raise forms.ValidationError(
                "El precio solamente puede contener números."
            )

        try:
            precio = Decimal(
                numero_limpio
            )

        except InvalidOperation:
            raise forms.ValidationError(
                "Ingresá un precio válido."
            )

        if precio <= 0:
            raise forms.ValidationError(
                "El precio debe ser mayor que cero."
            )

        if precio >= Decimal(
            "10000000000"
        ):
            raise forms.ValidationError(
                "El precio supera el límite permitido."
            )

        return precio

    def clean_descripcion(self):
        descripcion = " ".join(
            self.cleaned_data[
                "descripcion"
            ].split()
        )

        if len(descripcion) < 30:
            raise forms.ValidationError(
                "La descripción debe tener al menos 30 caracteres."
            )

        return descripcion

    def clean_foto_principal(self):
        imagen = self.cleaned_data.get(
            "foto_principal"
        )

        if not imagen:
            if not self.instance.pk:
                raise forms.ValidationError(
                    "Seleccioná una foto principal."
                )

            return imagen

        limite = 5 * 1024 * 1024

        if imagen.size > limite:
            raise forms.ValidationError(
                "La imagen no puede superar los 5 MB."
            )

        tipos_permitidos = {
            "image/jpeg",
            "image/png",
            "image/webp",
        }

        tipo_archivo = getattr(
            imagen,
            "content_type",
            "",
        )

        if (
            tipo_archivo
            and tipo_archivo
            not in tipos_permitidos
        ):
            raise forms.ValidationError(
                "La imagen debe ser JPG, PNG o WEBP."
            )

        return imagen

    def clean(self):
        datos = super().clean()

        departamento = datos.get(
            "departamento"
        )

        ciudad = datos.get(
            "ciudad"
        )

        latitud = datos.get(
            "latitud"
        )

        longitud = datos.get(
            "longitud"
        )

        ciudades_validas = (
            get_ciudades_for_departamento(
                departamento
            )
        )

        if (
            ciudad
            and ciudad
            not in ciudades_validas
        ):
            self.add_error(
                "ciudad",
                "La ciudad seleccionada no pertenece "
                "al departamento.",
            )

        if latitud is None:
            self.add_error(
                "latitud",
                "Seleccioná la ubicación en el mapa.",
            )

        if longitud is None:
            self.add_error(
                "longitud",
                "Seleccioná la ubicación en el mapa.",
            )

        if (
            latitud is not None
            and not Decimal("-90")
            <= latitud
            <= Decimal("90")
        ):
            self.add_error(
                "latitud",
                "La latitud seleccionada no es válida.",
            )

        if (
            longitud is not None
            and not Decimal("-180")
            <= longitud
            <= Decimal("180")
        ):
            self.add_error(
                "longitud",
                "La longitud seleccionada no es válida.",
            )

        tipo = datos.get(
            "tipo"
        )

        if tipo == "terreno":
            datos["dormitorios"] = 0
            datos["banos"] = 0
            datos["cochera"] = False

        return datos
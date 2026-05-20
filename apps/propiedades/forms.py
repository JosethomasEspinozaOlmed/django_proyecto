from django import forms
from .models import Propiedad
from decimal import Decimal, InvalidOperation


class PropiedadForm(forms.ModelForm):
    MONEDA_CHOICES = (
        ("USD", "Dólar (USD)"),
        ("PYG", "Guaraníes (PYG)"),
    )
    moneda = forms.ChoiceField(
        choices=MONEDA_CHOICES,
        required=True,
        initial="USD",
        widget=forms.Select(attrs={"class": "form-select", "required": True}),
    )
    departamento = forms.ChoiceField(
        choices=Propiedad.DEPARTAMENTO_CHOICES,
        required=True,
        widget=forms.Select(
            attrs={"class": "form-select departamento-select", "required": True}
        ),
    )
    precio = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control precio-input",
                "placeholder": "Ej: 1,200,000",
                "required": True,
                "inputmode": "decimal",
            }
        )
    )

    class Meta:
        model = Propiedad
        exclude = ["vendedor", "estado", "creado"]
        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: Casa en Asunción con jardín",
                    "required": True,
                }
            ),
            "tipo": forms.Select(attrs={"class": "form-select", "required": True}),
            # `precio` overridden above to allow formatted input
            "precio": forms.TextInput(
                attrs={
                    "class": "form-control precio-input",
                    "placeholder": "Ej: 1,200,000",
                    "required": True,
                    "inputmode": "decimal",
                }
            ),
            "ciudad": forms.TextInput(
                attrs={
                    "class": "form-control ciudad-input",
                    "placeholder": "Ej: Hohenau",
                    "list": "ciudades-list",
                    "required": True,
                    "autocomplete": "off",
                }
            ),
            "barrio": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: San Martin"}
            ),
            "direccion": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: Avda. España 123"}
            ),
            "ubicacion": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Pegá aquí el enlace de Google Maps",
                }
            ),
            "superficie": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: 180",
                    "required": True,
                }
            ),
            "dormitorios": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: 3",
                    "required": True,
                }
            ),
            "banos": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: 2",
                    "required": True,
                }
            ),
            "cochera": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Describí la propiedad...",
                    "rows": 5,
                    "required": True,
                }
            ),
            "foto_principal": forms.ClearableFileInput(
                attrs={"class": "form-control", "required": True}
            ),
        }
        labels = {
            "titulo": "Título",
            "tipo": "Tipo de propiedad",
            "precio": "Precio",
            "moneda": "Moneda",
            "departamento": "Departamento",
            "ciudad": "Ciudad",
            "barrio": "Barrio",
            "direccion": "Dirección",
            "superficie": "Superficie (m²)",
            "dormitorios": "Dormitorios",
            "banos": "Baños",
            "cochera": "¿Tiene cochera?",
            "descripcion": "Descripción",
            "foto_principal": "Foto principal",
        }

    def clean_precio(self):
        raw = self.cleaned_data.get("precio", "")
        if isinstance(raw, (int, float, Decimal)):
            return Decimal(raw)
        # eliminar separadores de miles y espacios
        cleaned = str(raw).replace(" ", "").replace(",", "")
        try:
            value = Decimal(cleaned)
        except InvalidOperation:
            raise forms.ValidationError("Precio inválido")
        return value

    def save(self, commit=True):
        instance = super().save(commit=False)
        # moneda y departamento vienen desde los campos del formulario
        moneda = self.cleaned_data.get("moneda")
        if moneda:
            instance.moneda = moneda
        departamento = self.cleaned_data.get("departamento")
        if departamento:
            instance.departamento = departamento
        # precio ya limpiado en clean_precio
        precio = self.cleaned_data.get("precio")
        if precio is not None:
            instance.precio = precio
        if commit:
            instance.save()
            self.save_m2m()
        return instance

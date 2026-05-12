from django import forms
from .models import Propiedad


class PropiedadForm(forms.ModelForm):
    class Meta:
        model = Propiedad
        exclude = ["vendedor", "estado", "creado"]
        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: Casa en Asunción con jardín",
                }
            ),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "precio": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Ej: 120000"}
            ),
            "ciudad": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: Asunción"}
            ),
            "barrio": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: Villa Morra"}
            ),
            "direccion": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: Avda. España 123"}
            ),
            "superficie": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Ej: 180"}
            ),
            "dormitorios": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Ej: 3"}
            ),
            "banos": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Ej: 2"}
            ),
            "cochera": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Describí la propiedad...",
                    "rows": 5,
                }
            ),
            "foto_principal": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "titulo": "Título",
            "tipo": "Tipo de propiedad",
            "precio": "Precio (USD)",
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

import re

from django import forms

from .models import Contacto


class ContactoForm(forms.ModelForm):

    class Meta:
        model = Contacto

        fields = [
            "contacto",
            "mensaje",
        ]

        labels = {
            "contacto": ("Teléfono o correo de contacto"),
            "mensaje": ("Mensaje para el vendedor"),
        }

        widgets = {
            "contacto": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": ("Ej: 0981 123456 o " "nombre@correo.com"),
                }
            ),
            "mensaje": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "maxlength": 1000,
                    "placeholder": ("Hola, quisiera recibir " "más información..."),
                }
            ),
        }

    def clean_contacto(self):
        contacto = self.cleaned_data["contacto"].strip()

        es_correo = re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            contacto,
        )

        numeros = re.sub(
            r"\D",
            "",
            contacto,
        )

        es_telefono = 9 <= len(numeros) <= 15

        if not es_correo and not es_telefono:
            raise forms.ValidationError("Ingresá un teléfono " "o correo válido.")

        return contacto

    def clean_mensaje(self):
        mensaje = " ".join(self.cleaned_data["mensaje"].split())

        if len(mensaje) < 15:
            raise forms.ValidationError(
                "El mensaje debe tener " "al menos 15 caracteres."
            )

        return mensaje

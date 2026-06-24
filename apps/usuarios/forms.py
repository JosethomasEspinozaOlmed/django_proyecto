import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class RegistroForm(UserCreationForm):
    first_name = forms.CharField(
        label="Nombre",
        max_length=80,
    )
    last_name = forms.CharField(
        label="Apellido",
        max_length=80,
    )
    email = forms.EmailField(
        label="Correo electrónico",
    )
    telefono = forms.CharField(
        label="Teléfono",
        max_length=20,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "telefono",
            "password1",
            "password2",
        )

        labels = {
            "username": "Nombre de usuario",
        }

        help_texts = {
            "username": "",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "first_name": "Ej: José",
            "last_name": "Ej: Espinoza",
            "username": "Elegí un nombre de usuario",
            "email": "nombre@correo.com",
            "telefono": "Ej: 0981 123456",
            "password1": "Creá una contraseña segura",
            "password2": "Repetí la contraseña",
        }

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": placeholders.get(name, ""),
                    "autocomplete": (
                        "new-password" if name.startswith("password") else "off"
                    ),
                }
            )

    def clean_first_name(self):
        nombre = self.cleaned_data["first_name"].strip()

        if len(nombre) < 2 or not re.search(
            r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]",
            nombre,
        ):
            raise forms.ValidationError("Ingresá un nombre válido.")

        return nombre.title()

    def clean_last_name(self):
        apellido = self.cleaned_data["last_name"].strip()

        if len(apellido) < 2 or not re.search(
            r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]",
            apellido,
        ):
            raise forms.ValidationError("Ingresá un apellido válido.")

        return apellido.title()

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo.")

        return email

    def clean_telefono(self):
        telefono = self.cleaned_data["telefono"].strip()
        numeros = re.sub(r"\D", "", telefono)

        if len(numeros) < 9 or len(numeros) > 15:
            raise forms.ValidationError("Ingresá un número de teléfono válido.")

        return telefono


class AccesoForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Tu nombre de usuario",
                "autocomplete": "username",
                "autofocus": True,
            }
        ),
    )

    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Tu contraseña",
                "autocomplete": "current-password",
            }
        ),
    )

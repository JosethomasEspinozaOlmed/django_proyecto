from django import forms
from django.contrib.auth.models import User
from .models import Perfil

class RegistroForm(forms.ModelForm):
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresá tu contraseña'
        })
    )

    telefono = forms.CharField(
        label='Teléfono',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 0981 123456'
        })
    )

    rol = forms.ChoiceField(
        choices=Perfil.ROL_CHOICES,
        label='Rol',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password']
        labels = {
            'first_name': 'Nombre completo',
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresá tu nombre completo'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Elegí un nombre de usuario'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresá tu correo electrónico'
            }),
        }
        help_texts = {
            'username': ''
        }
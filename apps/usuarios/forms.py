from django import forms
from django.contrib.auth.models import User
from .models import Perfil

class RegistroForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    telefono = forms.CharField(label='Teléfono')
    rol = forms.ChoiceField(choices=Perfil.ROL_CHOICES, label='Rol')

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password']
        labels = {
            'first_name': 'Nombre completo',
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
        }
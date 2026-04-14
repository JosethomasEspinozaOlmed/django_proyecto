from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, label='Nombre', required=True)
    last_name = forms.CharField(max_length=150, label='Apellido', required=True)
    email = forms.EmailField(label='Email', required=True)

    class Meta:
        model = UserProfile
        fields = ['role', 'phone', 'avatar', 'bio']
        labels = {
            'role': 'Rol en la plataforma',
            'phone': 'Teléfono / WhatsApp',
            'avatar': 'Foto de perfil',
            'bio': 'Sobre mí',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            'email',
            Row(
                Column('phone', css_class='col-md-6'),
                Column('role', css_class='col-md-6'),
            ),
            'bio',
            'avatar',
            Submit('submit', 'Guardar cambios', css_class='btn btn-primary mt-2'),
        )

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
        if commit:
            profile.save()
        return profile

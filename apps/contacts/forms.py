from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['sender_name', 'sender_email', 'sender_phone', 'message']
        labels = {
            'sender_name': 'Tu nombre',
            'sender_email': 'Email',
            'sender_phone': 'Teléfono / WhatsApp',
            'message': 'Mensaje',
        }
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Hola, me interesa la propiedad. ¿Está disponible para visitar?'
            }),
            'sender_name': forms.TextInput(attrs={'placeholder': 'Tu nombre completo'}),
            'sender_email': forms.EmailInput(attrs={'placeholder': 'tu@email.com'}),
            'sender_phone': forms.TextInput(attrs={'placeholder': '0981-123456'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('sender_name'),
            Row(
                Column('sender_email', css_class='col-md-6'),
                Column('sender_phone', css_class='col-md-6'),
            ),
            Field('message'),
            Submit('submit', 'Enviar mensaje', css_class='btn btn-primary w-100'),
        )

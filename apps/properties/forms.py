from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field, HTML
from .models import Property, PropertyPhoto


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'property_type', 'price', 'city', 'address',
            'latitude', 'longitude', 'bedrooms', 'bathrooms',
            'area_m2', 'has_garage', 'description', 'status',
        ]
        labels = {
            'title': 'Título del anuncio',
            'property_type': 'Tipo de propiedad',
            'price': 'Precio (USD)',
            'city': 'Ciudad',
            'address': 'Dirección',
            'latitude': 'Latitud (opcional)',
            'longitude': 'Longitud (opcional)',
            'bedrooms': 'Dormitorios',
            'bathrooms': 'Baños',
            'area_m2': 'Superficie (m²)',
            'has_garage': 'Tiene cochera',
            'description': 'Descripción',
            'status': 'Estado',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describí la propiedad en detalle...'}),
            'price': forms.NumberInput(attrs={'placeholder': '120000'}),
            'area_m2': forms.NumberInput(attrs={'placeholder': '180'}),
            'address': forms.TextInput(attrs={'placeholder': 'Ej: Av. España 1234, Villa Morra'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title', css_class='mb-3'),
            Row(
                Column('property_type', css_class='col-md-4'),
                Column('price', css_class='col-md-4'),
                Column('status', css_class='col-md-4'),
            ),
            Row(
                Column('city', css_class='col-md-6'),
                Column('address', css_class='col-md-6'),
            ),
            Row(
                Column('bedrooms', css_class='col-md-3'),
                Column('bathrooms', css_class='col-md-3'),
                Column('area_m2', css_class='col-md-3'),
                Column('has_garage', css_class='col-md-3 d-flex align-items-end pb-3'),
            ),
            Field('description', css_class='mb-3'),
            HTML('<hr><h6 class="text-muted mb-3">Ubicación en mapa (opcional)</h6>'),
            Row(
                Column('latitude', css_class='col-md-6'),
                Column('longitude', css_class='col-md-6'),
            ),
            HTML('<div id="map-picker" style="height:250px;border-radius:8px;margin-bottom:1rem;"></div>'),
            Submit('submit', 'Guardar propiedad', css_class='btn btn-primary btn-lg'),
        )


class PropertyPhotoForm(forms.ModelForm):
    class Meta:
        model = PropertyPhoto
        fields = ['image', 'is_cover']
        labels = {
            'image': 'Foto',
            'is_cover': 'Usar como foto principal',
        }


PropertyPhotoFormSet = forms.inlineformset_factory(
    Property,
    PropertyPhoto,
    form=PropertyPhotoForm,
    extra=5,
    max_num=10,
    can_delete=True,
)

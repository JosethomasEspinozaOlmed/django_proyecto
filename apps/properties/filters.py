import django_filters
from django import forms
from .models import Property, City


class PropertyFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Buscar',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar por título o descripción...'})
    )
    property_type = django_filters.ChoiceFilter(
        choices=[('', 'Todos los tipos')] + Property.TYPE_CHOICES,
        label='Tipo',
        empty_label=None
    )
    city = django_filters.ModelChoiceFilter(
        queryset=City.objects.all(),
        label='Ciudad',
        empty_label='Todas las ciudades'
    )
    price_min = django_filters.NumberFilter(
        field_name='price', lookup_expr='gte',
        label='Precio mínimo (USD)',
        widget=forms.NumberInput(attrs={'placeholder': '0'})
    )
    price_max = django_filters.NumberFilter(
        field_name='price', lookup_expr='lte',
        label='Precio máximo (USD)',
        widget=forms.NumberInput(attrs={'placeholder': '500000'})
    )
    bedrooms = django_filters.NumberFilter(
        field_name='bedrooms', lookup_expr='gte',
        label='Dormitorios mínimos'
    )

    class Meta:
        model = Property
        fields = ['property_type', 'city', 'price_min', 'price_max', 'bedrooms']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar propiedades activas por defecto
        self.queryset = self.queryset.filter(status='active')

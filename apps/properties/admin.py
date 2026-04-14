from django.contrib import admin
from .models import City, Property, PropertyPhoto


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'department']
    search_fields = ['name', 'department']


class PropertyPhotoInline(admin.TabularInline):
    model = PropertyPhoto
    extra = 3
    fields = ['image', 'thumbnail', 'is_cover', 'order']
    readonly_fields = ['thumbnail']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'property_type', 'price', 'city', 'status', 'views_count', 'created_at']
    list_filter = ['property_type', 'status', 'city']
    search_fields = ['title', 'description', 'seller__email']
    list_editable = ['status']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    inlines = [PropertyPhotoInline]
    fieldsets = (
        ('Información básica', {
            'fields': ('seller', 'title', 'description', 'property_type', 'status')
        }),
        ('Precio y ubicación', {
            'fields': ('price', 'city', 'address', 'latitude', 'longitude')
        }),
        ('Características', {
            'fields': ('bedrooms', 'bathrooms', 'area_m2', 'has_garage')
        }),
        ('Estadísticas', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

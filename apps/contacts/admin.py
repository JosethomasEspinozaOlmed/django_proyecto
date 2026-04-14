from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['sender_name', 'sender_email', 'property', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender_name', 'sender_email', 'property__title']
    list_editable = ['is_read']
    readonly_fields = ['created_at']

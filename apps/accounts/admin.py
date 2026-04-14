from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'verified', 'created_at']
    list_filter = ['role', 'verified']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'phone']
    list_editable = ['verified']

from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user_type', 'phone', 'location', 'rating', 'created_at')
    list_filter = ('user_type', 'created_at')
    search_fields = ('user__username', 'phone', 'location')
    autocomplete_fields = ('user',)
    readonly_fields = ('created_at',)

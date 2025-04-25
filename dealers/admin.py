from django.contrib import admin
from .models import Dealer

@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'user', 'is_verified', 'rating', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('company_name', 'user__username', 'address', 'website')
    autocomplete_fields = ('user',)
    readonly_fields = ('created_at', 'updated_at')

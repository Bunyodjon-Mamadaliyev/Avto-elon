from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'listing_title', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'listing__title', 'content')
    autocomplete_fields = ('sender', 'receiver', 'listing')
    readonly_fields = ('created_at',)

    def listing_title(self, obj):
        return obj.listing.title
    listing_title.short_description = 'Listing'

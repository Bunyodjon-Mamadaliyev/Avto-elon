from django.contrib import admin
from .models import PriceHistory

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing_title', 'price', 'currency', 'created_at')
    list_filter = ('currency', 'created_at')
    search_fields = ('listing__title',)
    autocomplete_fields = ('listing',)
    readonly_fields = ('created_at',)

    def listing_title(self, obj):
        return obj.listing.title
    listing_title.short_description = 'Listing'

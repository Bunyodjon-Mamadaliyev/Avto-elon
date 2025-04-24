from django.contrib import admin
from .models import SavedListing, ComparisonList


@admin.register(SavedListing)
class SavedListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'listing', 'created_at')
    search_fields = ('user__username', 'listing__title')
    list_filter = ('created_at',)
    autocomplete_fields = ('user', 'listing')
    readonly_fields = ('created_at',)


@admin.register(ComparisonList)
class ComparisonListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'listing_count', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    list_filter = ('created_at',)
    autocomplete_fields = ('user',)
    filter_horizontal = ('listings',)
    readonly_fields = ('created_at', 'updated_at')

    def listing_count(self, obj):
        return obj.listings.count()
    listing_count.short_description = 'Number of Listings'

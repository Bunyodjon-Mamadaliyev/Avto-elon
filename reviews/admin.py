from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'reviewer', 'reviewed_user', 'rating', 'listing_title', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = (
        'reviewer__username',
        'reviewed_user__username',
        'comment',
        'listing__title'
    )
    autocomplete_fields = ('reviewer', 'reviewed_user', 'listing')
    readonly_fields = ('created_at',)

    def listing_title(self, obj):
        return obj.listing.title if obj.listing else "No listing"
    listing_title.short_description = 'Listing'

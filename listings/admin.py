from django.contrib import admin
from .models import Listing, Image

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    fields = ('image', 'is_primary', 'order', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('order',)

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'seller', 'car_display', 'price', 'currency',
        'condition', 'is_negotiable', 'is_active', 'is_featured', 'views_count', 'created_at'
    )
    list_filter = ('currency', 'condition', 'is_active', 'is_featured', 'created_at')
    search_fields = ('title', 'description', 'seller__username', 'car__make__name', 'car__model__name', 'location')
    autocomplete_fields = ('seller', 'car')
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    inlines = [ImageInline]
    ordering = ('-created_at',)

    def car_display(self, obj):
        return f"{obj.car.year} {obj.car.make.name} {obj.car.model.name}"
    car_display.short_description = 'Car'

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'is_primary', 'order', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('listing__title',)
    autocomplete_fields = ('listing',)
    readonly_fields = ('created_at',)
    ordering = ('order',)


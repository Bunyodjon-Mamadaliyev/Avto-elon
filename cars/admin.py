from django.contrib import admin
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'make', 'model', 'fuel_type', 'transmission', 'drive_type', 'mileage', 'engine_size', 'power', 'color')
    list_filter = ('make', 'model', 'fuel_type', 'transmission', 'drive_type', 'year', 'body_type')
    search_fields = ('vin', 'make__name', 'model__name', 'color')
    autocomplete_fields = ('make', 'model', 'body_type', 'features')
    filter_horizontal = ('features',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

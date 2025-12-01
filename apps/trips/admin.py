from django.contrib import admin
from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('departure_city', 'arrival_city', 'departure_date', 'departure_time', 
                    'driver', 'available_seats', 'price_per_seat', 'status', 'transport_type')
    list_filter = ('status', 'transport_type', 'departure_date', 'accepts_pets', 'accepts_smoking')
    search_fields = ('departure_city', 'arrival_city', 'driver__username', 'driver__email')
    date_hierarchy = 'departure_date'
    ordering = ('-departure_date', '-departure_time')
    
    fieldsets = (
        ('Informations du trajet', {
            'fields': ('driver', 'transport_type', 'status')
        }),
        ('Itinéraire', {
            'fields': ('departure_city', 'departure_address', 'arrival_city', 'arrival_address')
        }),
        ('Date et heure', {
            'fields': ('departure_date', 'departure_time')
        }),
        ('Places et prix', {
            'fields': ('available_seats', 'price_per_seat')
        }),
        ('Options', {
            'fields': ('luggage_size', 'accepts_pets', 'accepts_smoking', 'description')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')

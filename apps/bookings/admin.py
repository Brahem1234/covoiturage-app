from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'passenger', 'trip', 'seats_booked', 'total_price', 
                    'status', 'booking_date')
    list_filter = ('status', 'booking_date', 'confirmation_date')
    search_fields = ('passenger__username', 'passenger__email', 'passenger_phone',
                     'trip__departure_city', 'trip__arrival_city')
    date_hierarchy = 'booking_date'
    ordering = ('-booking_date',)
    
    fieldsets = (
        ('Informations de réservation', {
            'fields': ('trip', 'passenger', 'status')
        }),
        ('Détails', {
            'fields': ('seats_booked', 'total_price', 'passenger_phone', 
                      'pickup_location', 'special_requests')
        }),
        ('Dates', {
            'fields': ('booking_date', 'confirmation_date')
        }),
    )
    
    readonly_fields = ('booking_date',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('trip', 'passenger', 'total_price')
        return self.readonly_fields

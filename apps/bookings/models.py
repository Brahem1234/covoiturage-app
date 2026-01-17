from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('cancelled', 'Annulée'),
        ('completed', 'Terminée'),
    ]
    
    trip = models.ForeignKey('trips.Trip', on_delete=models.CASCADE, related_name='bookings')
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_as_passenger')
    
    seats_booked = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.00)])
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    booking_date = models.DateTimeField(auto_now_add=True)
    confirmation_date = models.DateTimeField(null=True, blank=True)
    
    passenger_phone = models.CharField(max_length=15)
    pickup_location = models.CharField(max_length=255, blank=True)
    special_requests = models.TextField(blank=True)
    
    def __str__(self):
        return f"Réservation de {self.passenger.username} pour {self.trip}"

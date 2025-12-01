from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Trip(models.Model):
    TRANSPORT_TYPE_CHOICES = [
        ('car', 'Voiture'),
        ('bus', 'Bus'),
        ('train', 'Train'),
        ('van', 'Van/Minibus'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Actif'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé'),
    ]
    
    transport_type = models.CharField(max_length=20, choices=TRANSPORT_TYPE_CHOICES, default='car')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips_as_driver')
    departure_city = models.CharField(max_length=100)
    departure_address = models.CharField(max_length=255)
    arrival_city = models.CharField(max_length=100)
    arrival_address = models.CharField(max_length=255)
    
    departure_date = models.DateField()
    departure_time = models.TimeField()
    
    available_seats = models.PositiveIntegerField()
    price_per_seat = models.DecimalField(max_digits=6, decimal_places=2)
    
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Options supplémentaires
    luggage_size = models.CharField(max_length=50, default='Moyen')
    accepts_pets = models.BooleanField(default=False)
    accepts_smoking = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-departure_date', '-departure_time']
    
    def __str__(self):
        return f"{self.departure_city} → {self.arrival_city} - {self.departure_date}"

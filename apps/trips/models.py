from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from .choices import GOVERNORATE_CHOICES

User = get_user_model()

def validate_future_date(value):
    if value < timezone.now().date():
        raise ValidationError("La date de départ ne peut pas être dans le passé.")

class Trip(models.Model):
    recurring_pattern = models.ForeignKey('RecurringTrip', on_delete=models.SET_NULL, null=True, blank=True, related_name='instances')
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
    departure_city = models.CharField(max_length=100, choices=GOVERNORATE_CHOICES, verbose_name='Gouvernorat de départ')
    departure_address = models.CharField(max_length=255, verbose_name='Adresse de départ')
    arrival_city = models.CharField(max_length=100, choices=GOVERNORATE_CHOICES, verbose_name="Gouvernorat d'arrivée")
    arrival_address = models.CharField(max_length=255, verbose_name="Adresse d'arrivée")
    
    departure_date = models.DateField(validators=[validate_future_date])
    departure_time = models.TimeField()
    
    available_seats = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price_per_seat = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])
    
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    country = models.CharField(max_length=50, default='Tunisie', verbose_name='Pays')
    
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

class RecurringTrip(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Quotidien'),
        ('weekly', 'Hebdomadaire'),
    ]
    
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recurring_trips')
    
    # Itinéraire (identique à Trip)
    departure_city = models.CharField(max_length=100, choices=GOVERNORATE_CHOICES, verbose_name='Gouvernorat de départ')
    departure_address = models.CharField(max_length=255, verbose_name='Adresse de départ')
    arrival_city = models.CharField(max_length=100, choices=GOVERNORATE_CHOICES, verbose_name="Gouvernorat d'arrivée")
    arrival_address = models.CharField(max_length=255, verbose_name="Adresse d'arrivée")
    departure_time = models.TimeField()
    
    available_seats = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price_per_seat = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])
    
    # Recurrence rules
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField(validators=[validate_future_date])
    end_date = models.DateField()
    
    # For weekly: '0,2,4' for Monday, Wednesday, Friday
    days_of_week = models.CharField(max_length=20, blank=True, help_text="0=Lun, 1=Mar, ..., 6=Dim. Séparez par des virgules.")
    
    is_active = models.BooleanField(default=True)
    country = models.CharField(max_length=50, default='Tunisie', verbose_name='Pays')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError("La date de fin doit être après la date de début.")
        if self.frequency == 'weekly' and not self.days_of_week:
            raise ValidationError("Veuillez sélectionner au moins un jour de la semaine pour une fréquence hebdomadaire.")

    def __str__(self):
        return f"Répétition: {self.departure_city} → {self.arrival_city} ({self.get_frequency_display()})"

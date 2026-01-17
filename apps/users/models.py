from django.contrib.auth.models import AbstractUser
from django.db.models import Avg
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_past_date(value):
    if value and value > timezone.now().date():
        raise ValidationError("La date de naissance ne peut pas être dans le futur.")

class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Homme'),
        ('F', 'Femme'),
        ('O', 'Autre'),
    ]
    
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{8,15}$',
        message="Le numéro de téléphone doit être au format: '+99999999'. De 8 à 15 chiffres autorisés."
    )
    
    VERIFICATION_STATUS_CHOICES = [
        ('unverified', 'Non vérifié'),
        ('pending', 'En attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
    ]
    
    DOCUMENT_TYPE_CHOICES = [
        ('id_card', 'Carte d\'identité'),
        ('passport', 'Passeport'),
        ('driving_license', 'Permis de conduire'),
    ]
    
    phone_number = models.CharField(validators=[phone_validator], max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True, validators=[validate_past_date])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
    
    # Vérification d'identité
    identity_document = models.ImageField(upload_to='identity_docs/', blank=True, null=True)
    identity_document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, blank=True)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='unverified')
    is_verified = models.BooleanField(default=False)
    
    # Préférences conducteur
    is_driver = models.BooleanField(default=False)
    car_model = models.CharField(max_length=100, blank=True)
    car_color = models.CharField(max_length=50, blank=True)
    license_plate = models.CharField(max_length=20, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
    @property
    def average_rating(self):
        avg = self.reviews_received.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0

    @property
    def review_count(self):
        return self.reviews_received.count()

    @property
    def trips_count(self):
        return self.trips_driven.count()

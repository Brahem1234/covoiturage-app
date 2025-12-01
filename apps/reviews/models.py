from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Mauvais'),
        (2, '2 - Médiocre'),
        (3, '3 - Moyen'),
        (4, '4 - Bien'),
        (5, '5 - Excellent'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_written')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    trip = models.ForeignKey('trips.Trip', on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['author', 'trip']  # Un avis par trajet

    def __str__(self):
        return f"Avis de {self.author} pour {self.recipient} ({self.rating}/5)"

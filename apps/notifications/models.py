from django.db import models
from django.conf import settings

class Notification(models.Model):
    TYPES = [
        ('booking_created', 'Nouvelle réservation'),
        ('booking_cancelled', 'Réservation annulée'),
        ('booking_confirmed', 'Réservation confirmée'),
        ('trip_cancelled', 'Trajet annulé'),
        ('payment_received', 'Paiement reçu'),
        ('new_message', 'Nouveau message'),
    ]

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_notification_type_display()} pour {self.recipient}"

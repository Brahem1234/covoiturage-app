from django.db import models
from django.contrib.auth import get_user_model
from apps.bookings.models import Booking

User = get_user_model()

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Carte bancaire'),
        ('paypal', 'PayPal'),
        ('cash', 'Espèces'),
        ('bank_transfer', 'Virement bancaire'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('completed', 'Complété'),
        ('failed', 'Échoué'),
        ('refunded', 'Remboursé'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_made')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_received')
    
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='card')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Informations de transaction
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Paiement {self.amount}€ - {self.get_status_display()}"
    
    def mark_as_completed(self):
        """Marquer le paiement comme complété"""
        from django.utils import timezone
        self.status = 'completed'
        self.completed_date = timezone.now()
        self.save()
    
    def mark_as_failed(self):
        """Marquer le paiement comme échoué"""
        self.status = 'failed'
        self.save()
    
    def refund(self):
        """Rembourser le paiement"""
        from django.utils import timezone
        self.status = 'refunded'
        self.completed_date = timezone.now()
        self.save()

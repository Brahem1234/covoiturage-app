from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'notes']
        widgets = {
            'payment_method': forms.RadioSelect,
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Notes ou instructions spéciales...'}),
        }
        labels = {
            'payment_method': 'Mode de paiement',
            'notes': 'Notes (optionnel)',
        }


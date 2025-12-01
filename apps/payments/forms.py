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

class CardPaymentForm(forms.Form):
    """Formulaire pour paiement par carte (simulation)"""
    card_number = forms.CharField(
        max_length=16,
        widget=forms.TextInput(attrs={
            'placeholder': '1234 5678 9012 3456',
            'class': 'form-control',
        }),
        label='Numéro de carte'
    )
    card_holder = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nom sur la carte',
            'class': 'form-control',
        }),
        label='Titulaire de la carte'
    )
    expiry_date = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={
            'placeholder': 'MM/AA',
            'class': 'form-control',
        }),
        label='Date d\'expiration'
    )
    cvv = forms.CharField(
        max_length=3,
        widget=forms.PasswordInput(attrs={
            'placeholder': '123',
            'class': 'form-control',
        }),
        label='CVV'
    )

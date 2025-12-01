from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['seats_booked', 'passenger_phone', 'pickup_location', 'special_requests']
        labels = {
            'seats_booked': 'Nombre de places',
            'passenger_phone': 'Numéro de téléphone',
            'pickup_location': 'Lieu de prise en charge',
            'special_requests': 'Demandes spéciales',
        }
        widgets = {
            'seats_booked': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 2',
                'min': '1'
            }),
            'passenger_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: +216 12 345 678'
            }),
            'pickup_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse précise de prise en charge (optionnel)'
            }),
            'special_requests': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Bagages volumineux, animaux, etc. (optionnel)'
            }),
        }
       
        
    
    def __init__(self, *args, **kwargs):
        self.trip = kwargs.pop('trip', None)
        super().__init__(*args, **kwargs)
        
    def clean_seats_booked(self):
        seats = self.cleaned_data['seats_booked']
        if self.trip and seats > self.trip.available_seats:
            raise forms.ValidationError(f"Désolé, il ne reste que {self.trip.available_seats} places disponibles.")
        if seats < 1:
            raise forms.ValidationError("Vous devez réserver au moins une place.")
        return seats

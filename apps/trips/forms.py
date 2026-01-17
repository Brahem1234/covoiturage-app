from django import forms
from .models import Trip
from .choices import GOVERNORATE_CHOICES, GOVERNORATE_ADDRESSES

class TripCreateForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            'transport_type',
            'departure_city', 'departure_address',
            'arrival_city', 'arrival_address',
            'departure_date', 'departure_time',
            'available_seats', 'price_per_seat',
            'description', 'luggage_size',
            'accepts_pets', 'accepts_smoking'
        ]
        widgets = {
            'departure_date': forms.DateInput(attrs={'type': 'date'}),
            'departure_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class TripSearchForm(forms.Form):
    departure_city = forms.ChoiceField(
        choices=[('', 'Tous les gouvernorats')] + list(GOVERNORATE_CHOICES),
        required=False,
        label='Départ',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    arrival_city = forms.ChoiceField(
        choices=[('', 'Tous les gouvernorats')] + list(GOVERNORATE_CHOICES),
        required=False,
        label='Arrivée',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    departure_date = forms.DateField(
        required=False, 
        label='Date',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    transport_type = forms.ChoiceField(
        choices=[('', 'Tous')] + Trip.TRANSPORT_TYPE_CHOICES,
        required=False,
        label='Type de transport'
    )

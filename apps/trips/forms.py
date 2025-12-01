from django import forms
from .models import Trip

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
    departure_city = forms.CharField(required=False, label='Départ')
    arrival_city = forms.CharField(required=False, label='Arrivée')
    departure_date = forms.DateField(
        required=False, 
        label='Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    transport_type = forms.ChoiceField(
        choices=[('', 'Tous')] + Trip.TRANSPORT_TYPE_CHOICES,
        required=False,
        label='Type de transport'
    )

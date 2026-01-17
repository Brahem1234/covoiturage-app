from django import forms
from .models import Trip, RecurringTrip
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
            'accepts_pets', 'accepts_smoking', 'country'
        ]
        widgets = {
            'transport_type': forms.Select(attrs={'class': 'form-control'}),
            'departure_city': forms.Select(attrs={'class': 'form-control', 'id': 'id_departure_city'}),
            'departure_address': forms.Select(attrs={'class': 'form-control', 'id': 'id_departure_address'}),
            'arrival_city': forms.Select(attrs={'class': 'form-control', 'id': 'id_arrival_city'}),
            'arrival_address': forms.Select(attrs={'class': 'form-control', 'id': 'id_arrival_address'}),
            'departure_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'departure_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
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
        label='Type de transport',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class RecurringTripForm(forms.ModelForm):
    DAYS_CHOICES = [
        ('0', 'Lundi'),
        ('1', 'Mardi'),
        ('2', 'Mercredi'),
        ('3', 'Jeudi'),
        ('4', 'Vendredi'),
        ('5', 'Samedi'),
        ('6', 'Dimanche'),
    ]
    
    days_of_week_list = forms.MultipleChoiceField(
        choices=DAYS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Jours de la semaine"
    )

    class Meta:
        model = RecurringTrip
        fields = [
            'departure_city', 'departure_address',
            'arrival_city', 'arrival_address',
            'departure_time', 'available_seats',
            'price_per_seat', 'frequency',
            'start_date', 'end_date', 'country'
        ]
        widgets = {
            'departure_city': forms.Select(attrs={'class': 'form-control', 'id': 'id_recurring_departure_city'}),
            'departure_address': forms.Select(attrs={'class': 'form-control', 'id': 'id_recurring_departure_address'}),
            'arrival_city': forms.Select(attrs={'class': 'form-control', 'id': 'id_recurring_arrival_city'}),
            'arrival_address': forms.Select(attrs={'class': 'form-control', 'id': 'id_recurring_arrival_address'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'departure_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        frequency = cleaned_data.get('frequency')
        days = cleaned_data.get('days_of_week_list')
        
        if frequency == 'weekly' and not days:
            raise forms.ValidationError("Veuillez choisir au moins un jour.")
        
        if days:
            cleaned_data['days_of_week'] = ','.join(days)
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.days_of_week = self.cleaned_data.get('days_of_week', '')
        if commit:
            instance.save()
        return instance

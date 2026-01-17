from rest_framework import serializers
from .models import Trip
from apps.users.serializers import UserSerializer

class TripSerializer(serializers.ModelSerializer):
    driver = UserSerializer(read_only=True)
    
    class Meta:
        model = Trip
        fields = [
            'id', 'transport_type', 'driver', 'departure_city', 'departure_address',
            'arrival_city', 'arrival_address', 'departure_date', 'departure_time',
            'available_seats', 'price_per_seat', 'description', 'status'
        ]

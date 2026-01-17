from rest_framework import serializers
from .models import Booking
from apps.trips.serializers import TripSerializer
from apps.users.serializers import UserSerializer

class BookingSerializer(serializers.ModelSerializer):
    passenger = UserSerializer(read_only=True)
    trip = TripSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'trip', 'passenger', 'seats_booked', 'total_price',
            'status', 'booking_date'
        ]

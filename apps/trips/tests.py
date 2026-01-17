from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta, time
from django.contrib.auth import get_user_model
from .models import Trip

User = get_user_model()

class TripModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='driver', password='password')

    def test_valid_trip(self):
        trip = Trip(
            driver=self.user,
            departure_city='Tunis',
            departure_address='Rue 123',
            arrival_city='Sousse',
            arrival_address='Boulevard 456',
            departure_date=timezone.now().date(),
            departure_time=time(10, 0),
            available_seats=4,
            price_per_seat=15.00
        )
        try:
            trip.full_clean()
        except ValidationError as e:
            self.fail(f"ValidationError raised on valid trip: {e}")

    def test_past_departure_date(self):
        past_date = timezone.now().date() - timedelta(days=1)
        trip = Trip(
            driver=self.user,
            departure_city='Tunis',
            departure_address='Rue 123',
            arrival_city='Sousse',
            arrival_address='Boulevard 456',
            departure_date=past_date,
            departure_time=time(10, 0),
            available_seats=4,
            price_per_seat=15.00
        )
        with self.assertRaises(ValidationError):
            trip.full_clean()

    def test_invalid_seats(self):
        trip = Trip(
            driver=self.user,
            departure_city='Tunis',
            departure_address='Rue 123',
            arrival_city='Sousse',
            arrival_address='Boulevard 456',
            departure_date=timezone.now().date(),
            departure_time=time(10, 0),
            available_seats=0,
            price_per_seat=15.00
        )
        with self.assertRaises(ValidationError):
            trip.full_clean()

    def test_invalid_price(self):
        trip = Trip(
            driver=self.user,
            departure_city='Tunis',
            departure_address='Rue 123',
            arrival_city='Sousse',
            arrival_address='Boulevard 456',
            departure_date=timezone.now().date(),
            departure_time=time(10, 0),
            available_seats=4,
            price_per_seat=0.00
        )
        with self.assertRaises(ValidationError):
            trip.full_clean()

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import User

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            password='password123',
            email='test@example.com'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')

    def test_invalid_phone_number(self):
        user = User(username='testuser2', password='password123', phone_number='abc')
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_valid_phone_number(self):
        user = User(username='testuser3', password='password123', phone_number='+21699888777')
        try:
            user.full_clean()
        except ValidationError as e:
            self.fail(f"ValidationError raised on valid phone number: {e}")

    def test_future_dob(self):
        future_date = timezone.now().date() + timedelta(days=1)
        user = User(username='testuser4', password='password123', date_of_birth=future_date)
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_past_dob(self):
        past_date = timezone.now().date() - timedelta(days=365*20)
        user = User(username='testuser5', password='password123', date_of_birth=past_date)
        try:
            user.full_clean()
        except ValidationError as e:
            self.fail(f"ValidationError raised on valid past date of birth: {e}")

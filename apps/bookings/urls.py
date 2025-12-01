from django.urls import path
from . import views

urlpatterns = [
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('book/<int:trip_id>/', views.book_trip, name='book_trip'),
    path('<int:booking_id>/delete/', views.delete_booking, name='delete_booking'),
]

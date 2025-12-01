from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from .forms import BookingForm
from apps.trips.models import Trip

from apps.notifications.utils import create_notification

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(passenger=request.user).order_by('-booking_date')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def book_trip(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    
    if trip.driver == request.user:
        messages.error(request, "Vous ne pouvez pas réserver votre propre trajet.")
        return redirect('trip_detail', pk=trip.id)
        
    if trip.available_seats < 1:
        messages.error(request, "Ce trajet est complet.")
        return redirect('trip_detail', pk=trip.id)

    if request.method == 'POST':
        form = BookingForm(request.POST, trip=trip)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.trip = trip
            booking.passenger = request.user
            booking.total_price = booking.seats_booked * trip.price_per_seat
            booking.status = 'pending'  # Ou 'confirmed' selon la logique métier
            booking.save()
            
            # Mettre à jour les places disponibles
            trip.available_seats -= booking.seats_booked
            trip.save()
            
            # Notification au conducteur
            create_notification(
                recipient=trip.driver,
                notification_type='booking_created',
                title='Nouvelle réservation',
                message=f"{request.user.get_full_name() or request.user.username} a réservé {booking.seats_booked} place(s) pour votre trajet {trip.departure_city} - {trip.arrival_city}.",
                link=f"/trips/{trip.id}/"
            )
            
            messages.success(request, 'Votre réservation a été enregistrée avec succès !')
            return redirect('my_bookings')
    else:
        initial_data = {'passenger_phone': request.user.phone_number} if hasattr(request.user, 'phone_number') else {}
        form = BookingForm(initial=initial_data, trip=trip)
    
    return render(request, 'bookings/book_trip.html', {'form': form, 'trip': trip})

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, passenger=request.user)
    
    if booking.status == 'completed':
        messages.error(request, 'Impossible de supprimer une réservation terminée.')
        return redirect('my_bookings')
    
    if request.method == 'POST':
        # Remettre les places disponibles si la réservation n'était pas déjà annulée
        if booking.status != 'cancelled':
            trip = booking.trip
            trip.available_seats += booking.seats_booked
            trip.save()
            
            # Notification au conducteur
            create_notification(
                recipient=trip.driver,
                notification_type='booking_cancelled',
                title='Réservation annulée',
                message=f"{request.user.get_full_name() or request.user.username} a annulé sa réservation pour votre trajet {trip.departure_city} - {trip.arrival_city}.",
                link=f"/trips/{trip.id}/"
            )
        
        # Supprimer la réservation
        booking.delete()
        
        messages.success(request, 'Votre réservation a été supprimée avec succès.')
        return redirect('my_bookings')
    
    return render(request, 'bookings/delete_confirm.html', {'booking': booking})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from datetime import date

def home(request):
    now = timezone.now()
    current_date = now.date()
    current_time = now.time()
    
    # "Popular" trips: prioritized by number of confirmed bookings, then random/shuffled
    # This prevents brand new empty trips from appearing at the top immediately.
    popular_trips = Trip.objects.filter(status='active').exclude(id__in=[21, 22, 24]) \
        .filter(Q(departure_date__gt=current_date) | Q(departure_date=current_date, departure_time__gte=current_time)) \
        .annotate(booking_count=Count('bookings')) \
        .order_by('-booking_count', '?')[:4]
    
    today = date.today().isoformat()
    return render(request, 'trips/home.html', {'popular_trips': popular_trips, 'today': today})

def search_trips(request):
    form = TripSearchForm(request.GET or None)
    
    # Filter for active trips that haven't passed yet
    now = timezone.now()
    current_date = now.date()
    current_time = now.time()
    
    trips = Trip.objects.filter(status='active').filter(
        Q(departure_date__gt=current_date) | 
        Q(departure_date=current_date, departure_time__gte=current_time)
    ).select_related('driver')
    
    if form.is_valid():
        departure = form.cleaned_data.get('departure_city')
        arrival = form.cleaned_data.get('arrival_city')
        date_trip = form.cleaned_data.get('departure_date')
        transport_type = form.cleaned_data.get('transport_type')
        
        if departure:
            trips = trips.filter(departure_city__icontains=departure)
        if arrival:
            trips = trips.filter(arrival_city=arrival)
        if date_trip:
            trips = trips.filter(departure_date=date_trip)
        if transport_type:
            trips = trips.filter(transport_type=transport_type)
    
    context = {
        'form': form,
        'trips': trips,
    }
    return render(request, 'trips/search.html', context)

@login_required
def create_trip(request):
    # Determine type from POST or GET
    if request.method == 'POST':
        trip_type = request.POST.get('trip_type', 'single')
    else:
        trip_type = request.GET.get('type', 'single')

    if request.method == 'POST':
        form = TripCreateForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.driver = request.user
            trip.save()
            messages.success(request, 'Votre trajet a été publié avec succès!')
            return redirect('trip_detail', pk=trip.pk)
    else:
        # GET request
        form = TripCreateForm()
    
    return render(request, 'trips/create.html', {'form': form})

def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    return render(request, 'trips/detail.html', {
        'trip': trip,
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', '')
    })

@login_required
def my_trips(request):
    trips = Trip.objects.filter(driver=request.user).order_by('-departure_date', '-departure_time')
    return render(request, 'trips/my_trips.html', {'trips': trips})

@login_required
def edit_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk, driver=request.user)
    
    if request.method == 'POST':
        form = TripCreateForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre trajet a été modifié avec succès!')
            return redirect('trip_detail', pk=trip.pk)
    else:
        form = TripCreateForm(instance=trip)
    
    context = {
        'form': form,
        'trip': trip,
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', '')
    }
    return render(request, 'trips/edit.html', context)

@login_required
def delete_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk, driver=request.user)
    
    # Vérifier s'il y a des réservations actives
    if trip.bookings.filter(status__in=['pending', 'confirmed']).exists():
        messages.error(request, 'Impossible de supprimer ce trajet car il y a des réservations actives.')
        return redirect('my_trips')
    
    if request.method == 'POST':
        trip.delete()
        messages.success(request, 'Le trajet a été supprimé avec succès!')
        return redirect('my_trips')
    
    return render(request, 'trips/delete_confirm.html', {'trip': trip})

@login_required
def cancel_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk, driver=request.user)
    
    if request.method == 'POST':
        trip.status = 'cancelled'
        trip.save()
        
        # Récupérer les réservations actives avant de les annuler
        active_bookings = trip.bookings.filter(status__in=['pending', 'confirmed'])
        
        # Notifier chaque passager
        for booking in active_bookings:
            create_notification(
                recipient=booking.passenger,
                notification_type='trip_cancelled',
                title='Trajet annulé',
                message=f"Le trajet {trip.departure_city} - {trip.arrival_city} prévu le {trip.departure_date} a été annulé par le conducteur.",
                link=f"/trips/{trip.id}/"
            )
        
        # Annuler toutes les réservations associées
        active_bookings.update(status='cancelled')
        
        messages.success(request, 'Le trajet a été annulé. Toutes les réservations ont été annulées et les passagers notifiés.')
        return redirect('my_trips')
    
    return render(request, 'trips/cancel_confirm.html', {'trip': trip})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from datetime import date
from django.conf import settings
from decimal import Decimal
import math

from .models import Trip
from .forms import TripSearchForm, TripCreateForm, RecurringTripForm
from .tasks import generate_recurring_trips
from apps.notifications.utils import create_notification

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
        
        # Radius search logic
        search_lat = form.cleaned_data.get('lat')
        search_lng = form.cleaned_data.get('lng')
        radius = form.cleaned_data.get('radius')
        
        if search_lat is not None and search_lng is not None and radius:
            try:
                # Use float for math calculations, then convert back to Decimal for query consistency
                lat_delta_f = float(radius) / 111.0
                cos_factor = math.cos(math.radians(float(search_lat)))
                
                # Prevent division by zero
                if abs(cos_factor) < 0.0001:
                    cos_factor = 0.0001
                lng_delta_f = float(radius) / (111.0 * abs(cos_factor))
                
                lat_delta = Decimal(str(lat_delta_f))
                lng_delta = Decimal(str(lng_delta_f))
                
                # Convert inputs to strings then Decimal to ensure precision and type safety
                search_lat_decimal = Decimal(str(search_lat))
                search_lng_decimal = Decimal(str(search_lng))
                
                trips = trips.filter(
                    departure_lat__gte=search_lat_decimal - lat_delta,
                    departure_lat__lte=search_lat_decimal + lat_delta,
                    departure_lng__gte=search_lng_decimal - lng_delta,
                    departure_lng__lte=search_lng_decimal + lng_delta
                )
            except (ValueError, TypeError, ZeroDivisionError, Exception):
                pass # Fallback to no radius filtering if math fails

        elif departure:
            trips = trips.filter(departure_city=departure)

        if arrival:
            trips = trips.filter(arrival_city=arrival)
        if date_trip:
            trips = trips.filter(departure_date=date_trip)
        if transport_type:
            trips = trips.filter(transport_type=transport_type)
            
    # Apply sorting logic
    sort = request.GET.get('sort', 'earliest')
    if sort == 'price_asc':
        trips = trips.order_by('price_per_seat', 'departure_date', 'departure_time')
    elif sort == 'earliest':
        trips = trips.order_by('departure_date', 'departure_time')
    elif sort == 'closest':
        # Default to earliest for now (no coordinates/distance logic yet)
        trips = trips.order_by('departure_date', 'departure_time')
    elif sort == 'shortest':
        # Default to earliest for now (no duration logic yet)
        trips = trips.order_by('departure_date', 'departure_time')
    else:
        trips = trips.order_by('departure_date', 'departure_time')

    return render(request, 'trips/search.html', {
        'form': form, 
        'trips': trips,
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', '')
    })

@login_required
def create_trip(request):
    # Determine type from POST or GET
    if request.method == 'POST':
        trip_type = request.POST.get('trip_type', 'single')
    else:
        trip_type = request.GET.get('type', 'single')

    if request.method == 'POST':
        if trip_type == 'recurring':
            # Gérer la création d'un trajet récurrent
            form = RecurringTripForm(request.POST)
            # Create dummy Single form for context safety (unbound)
            single_form = TripCreateForm() 
            
            if form.is_valid():
                recurring = form.save(commit=False)
                recurring.driver = request.user
                recurring.save()
                
                # Déclencher la génération immédiate des trajets
                try:
                    generate_recurring_trips.delay()
                    messages.success(request, 'Votre trajet récurrent a été créé ! Les trajets pour les 30 prochains jours sont en cours de génération.')
                except Exception as e:
                    # Fallback if Celery/Redis is down: warn the user but the record is saved
                    messages.warning(request, 'Trajet récurrent créé, mais la génération automatique a échoué. Veuillez contacter le support.')
                return redirect('my_trips')
        else:
            # Gérer la création d'un trajet simple
            form = TripCreateForm(request.POST)
            # Create dummy Recurring form for context
            recurring_form = RecurringTripForm()
            
            if form.is_valid():
                trip = form.save(commit=False)
                trip.driver = request.user
                trip.save()
                messages.success(request, 'Votre trajet a été publié avec succès!')
                return redirect('trip_detail', pk=trip.pk)
    else:
        # GET request
        form = TripCreateForm()
        recurring_form = RecurringTripForm()

    # Prepare context correctly for the template
    if request.method == 'POST':
        if trip_type == 'recurring':
            recurring_form = form # The bound recurring form
            # Use data from recurring form to pre-fill the shared fields in the dummy form
            form = TripCreateForm(initial=recurring_form.data)
        else:
            # form is bound single form
            recurring_form = RecurringTripForm(initial=form.data) # Dummy recurring with shared data

    context = {
        'form': form,
        'recurring_form': recurring_form,
        'trip_type': trip_type,
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', '')
    }
    
    return render(request, 'trips/create.html', context)

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

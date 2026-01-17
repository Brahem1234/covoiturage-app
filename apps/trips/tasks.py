
from celery import shared_task
from django.utils import timezone
from .models import Trip, RecurringTrip
from datetime import timedelta
from django.db.models import Q

@shared_task
def generate_recurring_trips():
    """
    Génère les instances de trajets pour les 30 prochains jours
    basées sur les modèles récurrents actifs.
    """
    now = timezone.now().date()
    max_date = now + timedelta(days=30)
    
    recurring_trips = RecurringTrip.objects.filter(is_active=True)
    
    for pattern in recurring_trips:
        current_date = max(now, pattern.start_date)
        end_date = min(max_date, pattern.end_date)
        
        while current_date <= end_date:
            should_create = False
            
            if pattern.frequency == 'daily':
                should_create = True
            elif pattern.frequency == 'weekly':
                # days_of_week is '0,2,4' (0=Monday)
                # current_date.weekday() returns 0 for Monday
                if str(current_date.weekday()) in pattern.days_of_week.split(','):
                    should_create = True
            
            if should_create:
                # Vérifier si l'instance existe déjà
                exists = Trip.objects.filter(
                    recurring_pattern=pattern,
                    departure_date=current_date
                ).exists()
                
                if not exists:
                    Trip.objects.create(
                        recurring_pattern=pattern,
                        driver=pattern.driver,
                        departure_city=pattern.departure_city,
                        departure_address=pattern.departure_address,
                        arrival_city=pattern.arrival_city,
                        arrival_address=pattern.arrival_address,
                        departure_date=current_date,
                        departure_time=pattern.departure_time,
                        available_seats=pattern.available_seats,
                        price_per_seat=pattern.price_per_seat,
                        status='active'
                    )
            
            current_date += timedelta(days=1)

@shared_task
def cleanup_expired_trips():
    """
    Marque comme terminés les trajets dont la date/heure est passée.
    """
    now = timezone.now()
    current_date = now.date()
    current_time = now.time()
    
    # Trouver les trajets actifs qui sont passés
    # 1. Date passée (< today)
    # 2. Date d'aujourd'hui mais heure passée (< now)
    
    expired_trips = Trip.objects.filter(status='active').filter(
        Q(departure_date__lt=current_date) | 
        Q(departure_date=current_date, departure_time__lt=current_time)
    )
    
    count = expired_trips.count()
    if count > 0:
        expired_trips.update(status='completed')
        return f"{count} trajets marqués comme terminés."
    return "Aucun trajet expiré trouvé."

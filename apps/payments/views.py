from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from decouple import config
import stripe
import uuid

from .models import Payment
from .forms import PaymentForm
from apps.bookings.models import Booking

stripe.api_key = config('STRIPE_SECRET_KEY', default='')

@login_required
def create_checkout_session(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, passenger=request.user)
    
    # Créer l'objet Payment s'il n'existe pas
    payment, created = Payment.objects.get_or_create(
        booking=booking,
        defaults={
            'payer': request.user,
            'recipient': booking.trip.driver,
            'amount': booking.total_price,
            'status': 'pending',
            'payment_method': 'card'
        }
    )

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'tnd', # Dinar tunisien ou eur
                    'product_data': {
                        'name': f"Covoiturage: {booking.trip.departure_city} -> {booking.trip.arrival_city}",
                    },
                    'unit_amount': int(booking.total_price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('payment_success', args=[payment.id])) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('payment_detail', args=[payment.id])),
            metadata={'booking_id': booking.id, 'payment_id': payment.id}
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        messages.error(request, f"Erreur lors de la création de la session Stripe: {str(e)}")
        return redirect('my_bookings')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = config('STRIPE_WEBHOOK_SECRET', default='')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    # Gérer l'événement checkout.session.completed
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        payment_id = session.get('metadata', {}).get('payment_id')
        if payment_id:
            payment = Payment.objects.get(id=payment_id)
            payment.transaction_id = session.get('payment_intent')
            payment.mark_as_completed()
            
            # Mettre à jour le statut de la réservation
            payment.booking.status = 'confirmed'
            payment.booking.confirmation_date = timezone.now()
            payment.booking.save()
            
            # Notifications
            from apps.notifications.utils import create_notification
            
            # Au conducteur (destinataire du paiement)
            create_notification(
                recipient=payment.recipient,
                notification_type='payment_received',
                title='Paiement reçu',
                message=f"Vous avez reçu un paiement de {payment.amount} DT pour le trajet {payment.booking.trip.departure_city} - {payment.booking.trip.arrival_city}.",
                link=f"/payments/detail/{payment.id}/"
            )
            
            # Au passager (confirmation)
            create_notification(
                recipient=payment.payer,
                notification_type='booking_confirmed',
                title='Réservation confirmée',
                message=f"Votre paiement a été validé. Votre place pour le trajet vers {payment.booking.trip.arrival_city} est confirmée !",
                link=f"/bookings/my-bookings/"
            )

    return HttpResponse(status=200)

@login_required
def initiate_payment(request, booking_id):
    """Initier un paiement pour une réservation"""
    booking = get_object_or_404(Booking, pk=booking_id, passenger=request.user)
    
    # Vérifier si un paiement existe déjà
    if hasattr(booking, 'payment'):
        messages.info(request, 'Un paiement existe déjà pour cette réservation.')
        return redirect('payment_detail', payment_id=booking.payment.id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.payer = request.user
            payment.recipient = booking.trip.driver
            payment.amount = booking.total_price
            payment.status = 'pending'
            payment.save()
            
            # Rediriger vers la page de paiement selon la méthode
            if payment.payment_method == 'card':
                return redirect('create_checkout_session', booking_id=booking.id)
            elif payment.payment_method == 'cash':
                messages.success(request, 'Paiement en espèces confirmé. Payez le conducteur directement.')
                payment.status = 'pending'
                payment.save()
                return redirect('payment_success', payment_id=payment.id)
            else:
                messages.error(request, 'Méthode de paiement non supportée pour le moment.')
                return redirect('initiate_payment', booking_id=booking.id)
    else:
        form = PaymentForm()
    
    context = {
        'form': form,
        'booking': booking,
    }
    return render(request, 'payments/initiate.html', context)


@login_required
def payment_success(request, payment_id):
    """Page de confirmation de paiement"""
    payment = get_object_or_404(Payment, pk=payment_id, payer=request.user)
    
    context = {
        'payment': payment,
    }
    return render(request, 'payments/success.html', context)

@login_required
def payment_detail(request, payment_id):
    """Détails d'un paiement"""
    payment = get_object_or_404(Payment, pk=payment_id)
    
    # Vérifier que l'utilisateur est concerné par ce paiement
    if request.user != payment.payer and request.user != payment.recipient:
        messages.error(request, "Vous n'avez pas accès à ce paiement.")
        return redirect('home')
    
    context = {
        'payment': payment,
    }
    return render(request, 'payments/detail.html', context)

@login_required
def my_payments(request):
    """Liste des paiements de l'utilisateur"""
    payments_made = Payment.objects.filter(payer=request.user)
    payments_received = Payment.objects.filter(recipient=request.user)
    
    context = {
        'payments_made': payments_made,
        'payments_received': payments_received,
    }
    return render(request, 'payments/my_payments.html', context)

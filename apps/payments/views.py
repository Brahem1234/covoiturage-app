from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Payment
from .forms import PaymentForm, CardPaymentForm
from apps.bookings.models import Booking
import uuid

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
                return redirect('process_card_payment', payment_id=payment.id)
            elif payment.payment_method == 'cash':
                messages.success(request, 'Paiement en espèces confirmé. Payez le conducteur directement.')
                payment.status = 'pending'
                payment.save()
                return redirect('payment_success', payment_id=payment.id)
            else:
                return redirect('process_payment', payment_id=payment.id)
    else:
        form = PaymentForm()
    
    context = {
        'form': form,
        'booking': booking,
    }
    return render(request, 'payments/initiate.html', context)

@login_required
def process_card_payment(request, payment_id):
    """Traiter un paiement par carte (simulation)"""
    payment = get_object_or_404(Payment, pk=payment_id, payer=request.user)
    
    if request.method == 'POST':
        card_form = CardPaymentForm(request.POST)
        if card_form.is_valid():
            # Simulation de traitement de paiement
            payment.transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
            payment.mark_as_completed()
            
            # Mettre à jour le statut de la réservation
            payment.booking.status = 'confirmed'
            payment.booking.confirmation_date = timezone.now()
            payment.booking.save()
            
            messages.success(request, 'Paiement effectué avec succès !')
            return redirect('payment_success', payment_id=payment.id)
    else:
        card_form = CardPaymentForm()
    
    context = {
        'payment': payment,
        'card_form': card_form,
    }
    return render(request, 'payments/card_payment.html', context)

@login_required
def process_payment(request, payment_id):
    """Traiter un paiement (PayPal, virement, etc.)"""
    payment = get_object_or_404(Payment, pk=payment_id, payer=request.user)
    
    if request.method == 'POST':
        # Simulation de traitement
        payment.transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        payment.mark_as_completed()
        
        payment.booking.status = 'confirmed'
        payment.booking.confirmation_date = timezone.now()
        payment.booking.save()
        
        messages.success(request, 'Paiement effectué avec succès !')
        return redirect('payment_success', payment_id=payment.id)
    
    context = {
        'payment': payment,
    }
    return render(request, 'payments/process.html', context)

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

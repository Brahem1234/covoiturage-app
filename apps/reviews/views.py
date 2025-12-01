from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from apps.trips.models import Trip
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def leave_review(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    
    # Déterminer le destinataire (si je suis le conducteur, je note le passager, sinon je note le conducteur)
    # Note: Pour simplifier, on suppose ici qu'un passager note le conducteur.
    # Dans un système complet, il faudrait gérer la liste des passagers pour que le conducteur puisse les noter.
    
    if request.user == trip.driver:
        messages.error(request, "Les conducteurs ne peuvent pas encore laisser d'avis aux passagers dans cette version.")
        return redirect('trip_detail', pk=trip.id)
    
    recipient = trip.driver
    
    # Vérifier si l'utilisateur a déjà laissé un avis pour ce trajet
    existing_review = Review.objects.filter(author=request.user, trip=trip).exists()
    if existing_review:
        messages.warning(request, "Vous avez déjà laissé un avis pour ce trajet.")
        return redirect('trip_detail', pk=trip.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.recipient = recipient
            review.trip = trip
            review.save()
            messages.success(request, 'Votre avis a été publié avec succès !')
            return redirect('trip_detail', pk=trip.id)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/leave_review.html', {'form': form, 'trip': trip, 'recipient': recipient})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from .forms import UserRegisterForm, UserProfileForm, IdentityVerificationForm

class RateLimitedLoginView(LoginView):
    template_name = 'users/login.html'

    @method_decorator(ratelimit(key='ip', rate='5/m', block=True))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

@ratelimit(key='ip', rate='3/m', block=True)
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé pour {username} ! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})

@login_required
def verify_identity(request):
    if request.method == 'POST':
        form = IdentityVerificationForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.verification_status = 'pending'
            user.save()
            messages.success(request, 'Votre document a été soumis pour vérification. Le processus peut prendre jusqu\'à 24h.')
            return redirect('profile')
    else:
        form = IdentityVerificationForm(instance=request.user)
    
    return render(request, 'users/verify_identity.html', {'form': form})
def public_profile(request, username):
    user = get_object_or_404(User, username=username)
    reviews = user.reviews_received.all().order_by('-created_at')
    return render(request, 'users/public_profile.html', {
        'profile_user': user,
        'reviews': reviews
    })

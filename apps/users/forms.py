from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True, label="Prénom")
    last_name = forms.CharField(max_length=150, required=True, label="Nom")
    phone_number = forms.CharField(max_length=15, required=False, label="Téléphone")
    
    USER_TYPE_CHOICES = [
        ('passenger', 'Je cherche un trajet (Passager)'),
        ('driver', 'Je propose des trajets (Conducteur)'),
        ('both', 'Les deux (Passager et Conducteur)'),
    ]
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES, 
        required=True, 
        label="Je m'inscris en tant que",
        widget=forms.RadioSelect
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'user_type', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data.get('phone_number', '')
        
        # Définir is_driver selon le choix
        user_type = self.cleaned_data['user_type']
        if user_type in ['driver', 'both']:
            user.is_driver = True
        
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 
                  'gender', 'bio', 'profile_picture', 'is_driver', 'car_model', 
                  'car_color', 'license_plate']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class IdentityVerificationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['identity_document_type', 'identity_document']
        labels = {
            'identity_document_type': 'Type de document',
            'identity_document': 'Document d\'identité (Image)',
        }
        help_texts = {
            'identity_document': 'Veuillez télécharger une photo claire de votre pièce d\'identité.',
        }

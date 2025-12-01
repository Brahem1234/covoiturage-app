from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Partagez votre expérience...'}),
            'rating': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'rating': 'Note',
            'comment': 'Commentaire',
        }

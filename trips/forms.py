from django import forms
from .models import UserTripRequest, TripReview, BaseTrip


class UserTripRequestForm(forms.ModelForm):
    """Formulaire utilisé par l'utilisateur pour demander un voyage."""

    # Champ optionnel permettant de choisir un modèle de voyage défini par l'admin
    base_trip = forms.ModelChoiceField(
        queryset=BaseTrip.objects.all(),
        required=False,
        label="Modèle de voyage (optionnel)",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        """Configuration du formulaire basé sur le modèle UserTripRequest."""
        model = UserTripRequest
        fields = [
            'base_trip',
            'destination',
            'user_name',
            'days',
            'people_adults',
            'people_children',
            'preferences',
        ]
        labels = {
            'destination': 'Destination',
            'user_name': "Votre nom",
            'days': "Nombre de jours",
            'people_adults': "Nombre d'adultes",
            'people_children': "Nombre d'enfants",
            'preferences': "Préférences (séparées par des virgules)",
        }
        widgets = {
            'destination': forms.Select(attrs={'class': 'form-select'}),
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            'days': forms.NumberInput(attrs={'class': 'form-control'}),
            'people_adults': forms.NumberInput(attrs={'class': 'form-control'}),
            'people_children': forms.NumberInput(attrs={'class': 'form-control'}),
            'preferences': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class TripReviewForm(forms.ModelForm):
    """Formulaire pour laisser un avis sur un voyage."""

    class Meta:
        """Configuration du formulaire d'avis utilisateur."""
        model = TripReview
        fields = ['author_name', 'rating', 'text', 'user_suggested_price']
        labels = {
            'author_name': 'Nom',
            'rating': 'Note (1-5)',
            'text': 'Commentaire',
            'user_suggested_price': 'Prix estimé par vous (optionnel)',
        }
        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'user_suggested_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
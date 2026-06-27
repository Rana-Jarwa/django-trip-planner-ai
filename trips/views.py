from django.shortcuts import render, redirect, get_object_or_404
from .models import Destination, BaseTrip, UserTripRequest, AITripPlan
from .forms import UserTripRequestForm, TripReviewForm
from .utils import generate_ai_trip_plan


def home(request):
    """Page d'accueil avec un aperçu des voyages."""
    destinations = Destination.objects.all()[:6]
    base_trips = BaseTrip.objects.select_related('destination')[:6]
    context = {
        'destinations': destinations,
        'base_trips': base_trips,
    }
    return render(request, 'trips/home.html', context)


def trip_list(request):
    """Liste des voyages de base configurés par l'admin."""
    base_trips = BaseTrip.objects.select_related('destination').all()
    return render(request, 'trips/trip_list.html', {'base_trips': base_trips})


def trip_request_create(request):
    """Formulaire pour que l'utilisateur crée une demande de voyage."""
    if request.method == 'POST':
        form = UserTripRequestForm(request.POST)
        if form.is_valid():
            trip_request = form.save()

            base_trip = trip_request.base_trip or BaseTrip.objects.filter(destination=trip_request.destination).first()
            base_description = base_trip.description if base_trip else ""

           
            ai_text = generate_ai_trip_plan(
                destination_name=trip_request.destination.name,
                country=trip_request.destination.country,
                days=trip_request.days,
                people_adults=trip_request.people_adults,
                people_children=trip_request.people_children,
                preferences_text=trip_request.preferences,
                base_trip_description=base_description,
            )

            ai_plan = AITripPlan.objects.create(
                user_trip_request=trip_request,
                ai_prompt_sent="Plan généré avec Ollama (IA locale).",
                ai_response_raw=ai_text,
                ai_plan_structured=ai_text,
            )
            return redirect('trip_plan_detail', pk=ai_plan.pk)
    else:
        form = UserTripRequestForm()

    return render(request, 'trips/trip_request_form.html', {'form': form})


def trip_plan_detail(request, pk):
    """Affiche le plan IA et permet de laisser un avis."""
    ai_plan = get_object_or_404(AITripPlan, pk=pk)
    trip_request = ai_plan.user_trip_request
    reviews = ai_plan.reviews.all().order_by('-created_at')

    if request.method == 'POST':
        review_form = TripReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ai_trip_plan = ai_plan
            review.save()
            return redirect('trip_plan_detail', pk=ai_plan.pk)
    else:
        review_form = TripReviewForm()

    context = {
        'ai_plan': ai_plan,
        'trip_request': trip_request,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'trips/trip_plan_detail.html', context)
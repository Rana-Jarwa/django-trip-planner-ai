from django.contrib import admin
from .models import Destination, BaseTrip, UserTripRequest, AITripPlan, TripReview


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    """Configuration de l'affichage des destinations dans l'admin."""
    list_display = ('name', 'country', 'city', 'tags')
    search_fields = ('name', 'country', 'city', 'tags')


@admin.register(BaseTrip)
class BaseTripAdmin(admin.ModelAdmin):
    """Configuration de l'affichage des voyages de base."""
    list_display = ('title', 'destination', 'trip_type', 'base_price', 'min_days', 'max_days')
    list_filter = ('trip_type', 'destination')
    search_fields = ('title', 'destination__name')


@admin.register(UserTripRequest)
class UserTripRequestAdmin(admin.ModelAdmin):
    """Affichage des demandes de voyage utilisateurs."""
    list_display = ('user_name', 'destination', 'days', 'people_adults', 'people_children', 'created_at')
    list_filter = ('destination', 'days')
    search_fields = ('user_name', 'destination__name')


@admin.register(AITripPlan)
class AITripPlanAdmin(admin.ModelAdmin):
    """Affichage des plans IA générés."""
    list_display = ('user_trip_request', 'created_at')
    readonly_fields = ('ai_prompt_sent', 'ai_response_raw', 'ai_plan_structured')


@admin.register(TripReview)
class TripReviewAdmin(admin.ModelAdmin):
    """Affichage des avis utilisateurs."""
    list_display = ('author_name', 'ai_trip_plan', 'rating', 'user_suggested_price', 'approved_by_admin', 'created_at')
    list_filter = ('rating', 'approved_by_admin')
    search_fields = ('author_name', 'ai_trip_plan__user_trip_request__user_name')
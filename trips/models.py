from django.db import models


class Destination(models.Model):
    """Représente une ville ou région de destination pour les voyages."""
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    short_description = models.TextField(blank=True)
    main_image = models.ImageField(
        upload_to='destinations/',
        blank=True,
        null=True,
        help_text="Image principale de la destination."
    )
    tags = models.CharField(
        max_length=255,
        blank=True,
        help_text="Mots-clés séparés par des virgules (ex: nature, famille, montagne)."
    )

    class Meta:
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"

    def __str__(self):
        return self.name


class BaseTrip(models.Model):
    """Modèle de voyage défini par l'admin (base de travail pour l'IA)."""

    TRIP_TYPE_CHOICES = [
        ('family', 'Voyage en famille'),
        ('friends', 'Voyage entre amis'),
        ('couple', 'Voyage en couple'),
        ('solo', 'Voyage en solo'),
    ]

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='base_trips'
    )
    title = models.CharField(max_length=200)
    trip_type = models.CharField(
        max_length=20,
        choices=TRIP_TYPE_CHOICES,
        default='family'
    )
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Prix de base indiqué par l'admin."
    )
    min_days = models.PositiveIntegerField(default=1)
    max_days = models.PositiveIntegerField(default=7)
    default_tags = models.CharField(
        max_length=255,
        blank=True,
        help_text="Mots-clés par défaut pour ce voyage."
    )
    description = models.TextField(
        help_text="Description générale du voyage (servira de contexte pour l'IA)."
    )

    class Meta:
        verbose_name = "Voyage de base"
        verbose_name_plural = "Voyages de base"

    def __str__(self):
        return f"{self.title} - {self.destination.name}"


class UserTripRequest(models.Model):
    """Demande de voyage personnalisée faite par un utilisateur."""

    base_trip = models.ForeignKey(
        BaseTrip,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trip_requests'
    )
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='trip_requests'
    )

    user_name = models.CharField(
        max_length=100,
        help_text="Nom ou pseudo de l'utilisateur."
    )

    days = models.PositiveIntegerField(default=2)
    people_adults = models.PositiveIntegerField(default=2)
    people_children = models.PositiveIntegerField(default=0)

    preferences = models.CharField(
        max_length=255,
        blank=True,
        help_text="Préférences séparées par des virgules (ex: nature, aventure, gastronomie)."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Demande de voyage"
        verbose_name_plural = "Demandes de voyage"

    def __str__(self):
        return f"Demande de {self.user_name} à {self.destination.name}"


class AITripPlan(models.Model):
    """Plan de voyage généré (réel ou simulé) en réponse à une demande."""

    user_trip_request = models.OneToOneField(
        UserTripRequest,
        on_delete=models.CASCADE,
        related_name='ai_plan'
    )
    ai_prompt_sent = models.TextField(
        blank=True,
        help_text="Prompt envoyé au moteur d'IA."
    )
    ai_response_raw = models.TextField(
        blank=True,
        help_text="Réponse brute renvoyée par l'IA."
    )
    ai_plan_structured = models.TextField(
        blank=True,
        help_text="Plan de voyage mis en forme pour l'affichage."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Plan IA"
        verbose_name_plural = "Plans IA"

    def __str__(self):
        return f"Plan IA pour {self.user_trip_request}"


class TripReview(models.Model):
    """Avis utilisateur après avoir utilisé le plan de voyage."""

    ai_trip_plan = models.ForeignKey(
        AITripPlan,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(
        default=5,
        help_text="Note de 1 à 5."
    )
    text = models.TextField(blank=True)
    user_suggested_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prix estimé par l'utilisateur (optionnel)."
    )
    approved_by_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Avis de voyage"
        verbose_name_plural = "Avis de voyage"

    def __str__(self):
        return f"Avis de {self.author_name} ({self.rating}/5)"
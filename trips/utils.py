"""
Fonctions utilitaires pour générer des plans de voyage.

Pour l'instant, nous utilisons un générateur simple basé sur des règles,
sans appel à une API d'IA externe (OpenAI, Ollama, etc.).
Plus tard, on pourra remplacer ou enrichir cette logique.
"""

import requests
from django.conf import settings

def generate_ai_trip_plan(
    destination_name: str,
    country: str,
    days: int,
    people_adults: int,
    people_children: int,
    preferences_text: str,
    base_trip_description: str,
) -> str:
    """
    Fonction qui appelle Ollama (serveur local) pour générer
    un plan de voyage intelligent sous forme de texte structuré.
    """

    # Récupération du nom du modèle et de l'URL de base depuis les settings Django
    model_name = getattr(settings, "OLLAMA_MODEL_NAME", "llama3")
    base_url = getattr(settings, "OLLAMA_BASE_URL", "http://localhost:11434")

    # Construction du prompt en français, clair et détaillé.
    # On demande un plan jour par jour avec les lieux les plus célèbres.
    prompt = f"""
Tu es un expert en création de voyages sur mesure.
Génère un plan de voyage complet et structuré pour la destination suivante.

Destination : {destination_name}, {country}
Nombre de jours : {days}
Nombre d'adultes : {people_adults}
Nombre d'enfants : {people_children}
Préférences principales : {preferences_text or "aucune préférence particulière indiquée"}

Description de base du séjour (contexte) :
{base_trip_description}

Contraintes de génération :
- Le texte doit être en français.
- Le plan doit être organisé jour par jour.
- Pour chaque jour, indique clairement trois moments :
  * Matin
  * Après-midi
  * Soirée
- Propose des activités adaptées au type de voyageurs (adultes / enfants).
- Utilise les lieux les plus connus et intéressants de {destination_name}.
- Donne des suggestions réalistes (pas de lieux imaginaires).
- Le ton doit être chaleureux et informatif.

Format souhaité (exemple de structure) :
Jour 1 :
Matin : ...
Après-midi : ...
Soirée : ...

Jour 2 :
Matin : ...
Après-midi : ...
Soirée : ...

Respecte cette structure dans ta réponse.
"""

    # Préparation de la requête HTTP vers l'API locale d'Ollama (/api/generate).
    url = f"{base_url}/api/generate"

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,      # on récupère la réponse en une fois
        "temperature": 0.3,   # texte plus stable, moins aléatoire
    }

    try:
        response = requests.post(url, json=payload, timeout=120)
    except requests.RequestException as e:
        # Gestion des erreurs réseau (Ollama non lancé, problème de connexion, etc.)
        return (
            "Erreur lors de l'appel à Ollama (serveur local). "
            "Vérifiez que Ollama est bien lancé et accessible.\n"
            f"Détails techniques : {e}"
        )

    if response.status_code != 200:
        # Gestion des codes d'erreur HTTP renvoyés par Ollama
        return (
            "La génération du plan de voyage via Ollama a échoué. "
            f"Code HTTP : {response.status_code}\n"
            f"Réponse : {response.text}"
        )

    # L'API /api/generate renvoie un JSON avec la clé 'response'
    data = response.json()
    ai_text = data.get("response", "").strip()

    if not ai_text:
        return (
            "Ollama a répondu, mais le texte généré est vide. "
            "Essayez de reformuler les préférences ou la description de base."
        )

    return ai_text
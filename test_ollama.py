import requests

def test_ollama_ai_trip_plan():
    """
    Exemple simple : on demande à Ollama de proposer lui-même
    un plan de voyage en français.
    """

    model_name = "llama3"  # adapte au modèle que tu utilises
    base_url = "http://localhost:11434"
    url = f"{base_url}/api/generate"

    prompt = """
Tu es un expert en organisation de voyages.
Propose un séjour complet pour découvrir Genève en Suisse.

Tu dois :
- Choisir toi-même une durée raisonnable (par exemple entre 3 et 5 jours).
- Proposer un plan de voyage jour par jour.
- Pour chaque jour, indiquer clairement les activités du matin, de l'après-midi et de la soirée.
- Utiliser uniquement des lieux réalistes et connus à Genève et autour du lac Léman.
- Écrire tout le texte en français.
- Adopter un ton chaleureux et informatif.

Écris directement le plan sans expliquer ta réflexion interne.
"""

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.7,
    }

    print("=== Envoi de la requête à Ollama... ===")
    response = requests.post(url, json=payload, timeout=120)

    print(f"Code HTTP : {response.status_code}")
    try:
        data = response.json()
    except Exception as e:
        print("Impossible de décoder la réponse en JSON :", e)
        print("Texte brut de la réponse :")
        print(response.text)
        return

    print("=== JSON complet renvoyé par Ollama ===")
    print(data)

    ai_text = data.get("response", "").strip()

    if not ai_text:
        print(">>> Le champ 'response' est vide. Voici le JSON complet pour diagnostic.")
        return

    print("\n=== Réponse générée par l'IA (Ollama) ===\n")
    print(ai_text)


if __name__ == "__main__":
    test_ollama_ai_trip_plan()
# AI Trip Planner – Django + Ollama

**AI Trip Planner** est une application web développée avec Django

qui permet de créer des programmes de voyage personnalisés en quelques clics.

L’utilisateur choisit une destination, le nombre de jours, le profil des voyageurs

(adultes, enfants) et ses préférences (nature, culture, gastronomie, etc.).

L’application génère ensuite un plan de voyage structuré jour par jour,

avec des suggestions d’activités matin / après-midi / soirée.

Une intégration optionnelle avec **Ollama** (IA locale) permet de générer

automatiquement le contenu des plans en français, en se basant sur les préférences

de l’utilisateur et la destination choisie.

---

## Fonctionnalités principales

- Gestion des destinations (pays, ville, description courte, image).

- Modèles de voyages (durée, type de séjour, points forts, budget de base).

- Formulaire utilisateur pour créer une demande de voyage.

- Génération automatique d’un plan de voyage :

  - Version simple basée sur des règles internes.

  - Version intelligente via une IA locale (Ollama) lorsque disponible.

- Interface en français, optimisée pour un affichage de gauche à droite (LTR).

- Intégration Django admin pour gérer facilement le contenu.

---

## Structure du projet

Le projet est organisé de la façon suivante :

- `trip_ai_planner/`  

  - `settings.py` – configuration principale de Django.  

  - `urls.py` – routes globales du projet.  

- `trips/`  

  - `models.py` – modèles de données (Destination, UserTripRequest, AITripPlan, etc.).  

  - `views.py` – vues pour la page d’accueil, le formulaire de voyage et les détails du plan.  

  - `utils.py` – fonctions utilitaires pour générer les plans de voyage (avec ou sans IA).  

  - `urls.py` – routes propres à l’application de voyages.  

  - `templates/trips/` – gabarits HTML (base, accueil, formulaires, détails des plans).  

- `templates/` (si utilisé) – gabarits HTML partagés.  

- `static/` – fichiers statiques (CSS, images, JS).  

- `requirements.txt` – dépendances Python du projet.  

- `.env` – variables d’environnement (non versionné, voir `.gitignore`).  

---

## Installation et exécution en local

### Prérequis

- Python 3 installé sur votre machine.  

- Git installé (pour cloner le projet depuis GitHub).  

### Étapes

1. Cloner le projet depuis GitHub :

   ```bash

   git clone [https://github.com/<votre-utilisateur>/django-trip-planner-ai.git](https://github.com/<votre-utilisateur>/django-trip-planner-ai.git)

   cd django-trip-planner-ai

   ```

2. Créer et activer un environnement virtuel (Windows) :

   ```bash

   python -m venv venv

   .\venv\Scripts\activate

   ```

3. Installer les dépendances Python :

   ```bash

   pip install -r requirements.txt

   ```

4. Appliquer les migrations de base de données :

   ```bash

   python [manage.py](http://manage.py) migrate

   ```

5. (Optionnel) Créer un super-utilisateur pour accéder au Django admin :

   ```bash

   python [manage.py](http://manage.py) createsuperuser

   ```

6. Lancer le serveur de développement :

   ```bash

   python [manage.py](http://manage.py) runserver

   ```

7. Ouvrir l’application dans le navigateur :

   - Page d’accueil : `http://127.0.0.1:8000/`  

   - Formulaire de demande de voyage : `http://127.0.0.1:8000/request/`  

   - Interface d’administration : `http://127.0.0.1:8000/admin/`

---

## Intégration avec l’IA locale (Ollama)

L’intégration avec Ollama est optionnelle et fonctionne en local :

1. Installer Ollama suivant la documentation officielle. [web:141][web:154]  

2. Télécharger un modèle compatible, par exemple :

   ```bash

   ollama pull llama3

   ```

3. S’assurer que Ollama est disponible sur `localhost:11434`. [web:196]

4. Configurer le projet Django (dans `settings.py`) :

   ```python

   OLLAMA_MODEL_NAME = "llama3"

   OLLAMA_BASE_URL = "[http://localhost:11434](http://localhost:11434)"

   ```

5. Utiliser les fonctions de `trips/utils.py` pour appeler l’API Ollama

   et générer automatiquement les plans de voyage en français.

Si Ollama n’est pas disponible, le projet fonctionne toujours avec le générateur

simple basé sur des règles internes.

---

## Déploiement

Ce projet est conçu pour un usage local et pour être présenté dans un portfolio.

Il peut ensuite être déployé sur un serveur (Railway, Render, VPS, etc.) en suivant

les bonnes pratiques de déploiement Django : configuration de la base de données,

collecte des fichiers statiques, utilisation d’un serveur WSGI/ASGI, etc. [web:209][web:214]

---

## Licence

Ce projet est publié sous licence MIT (ou autre licence à définir).

Voir le fichier `LICENSE` pour plus de détails.
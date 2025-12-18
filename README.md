# SoftDesk API 🚀

API RESTful développée avec **Django REST Framework** pour gérer des problèmes techniques (Issue Tracking System). Cette application permet aux utilisateurs de gérer des projets, d'ajouter des contributeurs, et de suivre des problèmes (issues) et des commentaires.

## 📋 Fonctionnalités

* **Authentification JWT :** Système sécurisé par tokens (Access & Refresh) via `djangorestframework-simplejwt`.
* **Gestion des Utilisateurs :** Inscription respectant les normes RGPD (âge minimum, consentement).
* **Gestion des Projets :** Création de projets (Back-end, Front-end, iOS, Android).
* **Permissions Avancées :**
    * L'auteur d'une ressource a tous les droits (Lecture/Écriture/Suppression).
    * Les contributeurs d'un projet ont un accès en lecture seule.
    * Les utilisateurs externes n'ont aucun accès.
* **Suivi des Problèmes :** Gestion des tâches, bugs et améliorations.

## 🛠️ Prérequis

* Python 3.x
* Git
* Pipenv (Recommandé pour la gestion des environnements virtuels)

## ⚙️ Installation

Ce projet utilise **Pipenv** pour une gestion moderne et sécurisée des dépendances.

### 1. Cloner le projet

```bash
git clone https://github.com/Freddy0ne1/SoftDesk
cd SoftDesk
```

### 2. Installer les dépendances

#### Option A : Avec Pipenv (Recommandé)

Si vous n'avez pas Pipenv, installez-le :

```bash
pip install pipenv
```

Installez ensuite l'environnement et les dépendances :

```bash
pipenv install
```

Activez l'environnement virtuel :

```bash
pipenv shell
```

#### Option B : Méthode Classique (venv & pip)

Si vous préférez ne pas utiliser Pipenv :

**Windows :**
```bash
python -m venv env
```

```bash
env\Scripts\activate
```

```bash
pip install -r requirements.txt
```

**Mac / Linux :**
```bash
python3 -m venv env
```

```bash
source env/bin/activate
```

```bash
pip install -r requirements.txt
```

### 3. Configurer la base de données

Appliquez les migrations pour créer les tables nécessaires (SQLite par défaut) :

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

### 4. Créer un administrateur (Superuser)

Pour accéder à l'interface d'administration Django :

```bash
python manage.py createsuperuser
```

### 5. Lancer le serveur

```bash
python manage.py runserver
```

L'API est maintenant accessible à l'adresse : **http://127.0.0.1:8000/**

## 🔑 Utilisation de l'API

Toutes les requêtes (sauf l'inscription et le login) nécessitent une authentification. Vous devez inclure le header suivant dans vos requêtes :

```
Authorization: Bearer <votre_access_token>
```

### Authentification

* **Inscription :** `POST /api/users/`
* **Connexion (Obtenir les tokens) :** `POST /api/token/`
    * Renvoie un `access token` (valide 1h) et un `refresh token` (valide 24h).
* **Rafraîchir le token :** `POST /api/token/refresh/`

### Endpoints Principaux

| Ressource | URL | Méthodes Autorisées |
|-----------|-----|---------------------|
| Projets | `/api/projects/` | GET, POST |
| Détail Projet | `/api/projects/{id}/` | GET, PUT, DELETE |
| Contributeurs | `/api/contributors/` | GET, POST |
| Issues | `/api/issues/` | GET, POST |
| Commentaires | `/api/comments/` | GET, POST |

## 📚 Documentation

Pour plus de détails sur l'utilisation de chaque endpoint, consultez la documentation interactive de l'API disponible à l'adresse suivante une fois le serveur lancé :

* **Swagger UI :** http://127.0.0.1:8000/swagger/
* **ReDoc :** http://127.0.0.1:8000/redoc/

## 🔒 Sécurité & Conformité RGPD

* Âge minimum requis pour l'inscription : 15 ans
* Consentement obligatoire pour le traitement des données
* Système de permissions granulaires
* Authentification sécurisée par JWT


## 👤 Auteur

**Freddy0ne1**
* GitHub : [@Freddy0ne1](https://github.com/Freddy0ne1)

---

*Développé avec ❤️ en utilisant Django REST Framework*
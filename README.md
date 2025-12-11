# SoftDesk API

API RESTful développée avec Django REST Framework pour la gestion de projets et de tickets de support technique.

## Technologies utilisées

- **Python** avec Django
- **Django REST Framework** pour l'API
- **PyJWT** pour l'authentification par tokens
- **Pipenv** pour la gestion des dépendances

## Prérequis

- Python 3.x
- Pipenv

## Installation

### 1. Installer les dépendances
```bash
pipenv install
```

Si le Pipfile n'est pas configuré, installez manuellement les packages nécessaires :
```bash
pipenv install django djangorestframework pyjwt
```

### 2. Activer l'environnement virtuel
```bash
pipenv shell
```

### 3. Configurer la base de données

Créer les migrations :
```bash
python manage.py makemigrations
```

Appliquer les migrations :
```bash
python manage.py migrate
```

### 4. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

Suivez les instructions pour définir un nom d'utilisateur et un mot de passe.

### 5. Lancer le serveur de développement
```bash
python manage.py runserver
```

Le serveur sera accessible à l'adresse : `http://127.0.0.1:8000/`

## Accès

- **API** : `http://127.0.0.1:8000/api/`
- **Interface d'administration** : `http://127.0.0.1:8000/admin/`

## Authentification

L'API utilise l'authentification par token JWT (JSON Web Token).
Mais pour le moment je n'ai rien fait


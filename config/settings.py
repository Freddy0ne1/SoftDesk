"""
Django settings for config project.

Fichier de configuration principal du projet.
Contient les réglages pour la sécurité (JWT), la base de données, 
les applications installées et le Green IT (Pagination).
"""

from pathlib import Path
# Nécessaire pour définir la durée de vie du Token
from datetime import timedelta 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-s10^74_$f6f#2u)fa$ei9o%drrb-omryq=t#)ukkz5nj!v1is_"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Framework pour créer l'API REST
    "rest_framework",
    # Librairie pour gérer les Tokens JWT (optionnelle ici si pas utilisée dans les modèles, mais bonne pratique)
    "rest_framework_simplejwt", 
    # Nos applications locales
    "authentication",
    "projects",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# Utilisation de SQLite pour le développement (léger, fichier unique)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# Sécurité : Django vérifie la robustesse des mots de passe par défaut
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

# SÉCURITÉ / RGPD :
# Indique à Django d'utiliser notre modèle User personnalisé (avec gestion de l'âge et consentements)
AUTH_USER_MODEL = "authentication.User"

# CONFIGURATION DE L'API REST
REST_FRAMEWORK = {
    # GREEN IT :
    # On active la pagination par défaut pour éviter de charger des milliers de lignes inutilement.
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10, # Limite fixée à 10 éléments par page
    
    # SÉCURITÉ OWASP :
    # On force l'utilisation de JWT (JSON Web Token) pour l'authentification.
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

# CONFIGURATION DES TOKENS JWT (OWASP)
# Il est important de limiter la durée de vie des tokens pour limiter les risques en cas de vol.
SIMPLE_JWT = {
    # Access Token : Courte durée (ex: 30 min). L'utilisateur doit le rafraîchir souvent.
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    # Refresh Token : Durée plus longue (ex: 1 jour) pour ne pas forcer la reconnexion trop souvent.
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    # Algorithme de signature cryptographique robuste
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}
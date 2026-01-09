from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Modèle utilisateur personnalisé.
    Il étend le modèle standard AbstractUser de Django pour ajouter des informations
    spécifiques au métier (âge, consentements RGPD, etc.) sans réécrire toute la logique d'authentification.
    """

    # Date de naissance facultative (null=True pour la BDD, blank=True pour la validation des formulaires/API)
    birth_date = models.DateField(null=True, blank=True, verbose_name="Date de naissance")

    # Champs de consentement (Conformité RGPD et préférences utilisateur)
    can_be_contacted = models.BooleanField(default=False, verbose_name="Peut être contacté")
    can_data_be_shared = models.BooleanField(default=False, verbose_name="Données partageables")

    # Horodatage automatique : auto_now_add=True enregistre la date uniquement à la création de l'objet
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def __str__(self):
        """
        Représentation textuelle de l'objet (utilisée dans l'interface d'admin Django et les logs).
        """
        return self.username
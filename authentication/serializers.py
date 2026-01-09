from rest_framework import serializers
from authentication.models import User
from datetime import date

class UserSerializer(serializers.ModelSerializer):
    """
    Sérailiseur pour la gestion des utilisateurs (Inscription et Profil).
    Gère la validation de l'âge et le hachage sécurisé du mot de passe.
    """

    # Configuration du champ date de naissance :
    # - format : Format d'affichage dans le JSON de réponse (JJ-MM-AAAA).
    # - input_formats : Formats acceptés lors de l'envoi de données (flexibilité).
    birth_date = serializers.DateField(
        format='%d-%m-%Y',  
        input_formats=[
            '%d-%m-%Y',     
            '%d/%m/%Y',     
            '%Y-%m-%d',     
        ],
        required=False
    )
   
    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name", "email", "birth_date", "can_be_contacted", "can_data_be_shared"]
        
        # extra_kwargs permet de configurer des champs sans les redéfinir entièrement au-dessus.
        # - write_only : Le mot de passe peut être écrit (POST) mais ne sera jamais lu (GET) pour la sécurité.
        # - style : Indique à l'interface navigable (Browsable API) de masquer la saisie.
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}}
        }

    def validate_birth_date(self, value):
        """
        Validation métier personnalisée.
        Règle : L'utilisateur doit avoir au moins 15 ans pour s'inscrire.
        """
        if value:
            today = date.today()
            # Calcul précis de l'âge :
            # On soustrait 1 à l'année si l'anniversaire n'est pas encore passé cette année.
            # (La comparaison de tuples renvoie True (1) ou False (0)).
            age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            
            if age < 15:
                raise serializers.ValidationError("L'utilisateur doit avoir au moins 15 ans.")
        return value

    def create(self, validated_data):
        """
        Surcharge de la méthode de création standard.
        
        Pourquoi ?
        Par défaut, le ModelSerializer utilise User.objects.create(), qui stockerait
        le mot de passe en clair.
        On utilise ici User.objects.create_user() pour assurer le hachage automatique du mot de passe.
        """
        return User.objects.create_user(**validated_data)
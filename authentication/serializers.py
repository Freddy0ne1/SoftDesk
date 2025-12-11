from rest_framework import serializers
from authentication.models import User
from datetime import date

class UserSerializer(serializers.ModelSerializer):
    """
    Serialiseur pour l'utilisateur.
    """
    # On force le format Jour-Mois-Année
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
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}}
        }

    def validate_birth_date(self, value):
        """
        Vérifie que l'utilisateur a au moins 15 ans.
        Cette fonction est appelée automatiquement par le Serializer.
        """
        if value:
            today = date.today()
            age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if age < 15:
                raise serializers.ValidationError("L'utilisateur doit avoir au moins 15 ans.")
        return value

    def create(self, validated_data):
        """
        Crée un utilisateur avec les données validées.
        Cette fonction est appelée automatiquement par le Serializer.
        """
        return User.objects.create_user(**validated_data)
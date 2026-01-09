from rest_framework.permissions import BasePermission


class IsOwnerOrSuperUser(BasePermission):
    """
    Permission personnalisée pour la gestion des profils utilisateurs.
    
    Règle :
    - Un superutilisateur (Admin) a tous les droits.
    - Un utilisateur standard ne peut accéder qu'à SON propre profil (obj == user).
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Vérifie les droits sur une instance d'objet spécifique (ici, un User).
        """
        # 1. Accès inconditionnel pour le superuser (Admin)
        if request.user.is_superuser:
            return True
            
        # 2. Vérification de propriété :
        # On compare l'objet demandé (obj) avec l'utilisateur connecté (request.user).
        # Cela fonctionne car 'obj' est ici une instance du modèle User.
        return obj == request.user
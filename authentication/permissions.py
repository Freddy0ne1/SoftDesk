from rest_framework.permissions import BasePermission


class IsOwnerOrSuperUser(BasePermission):
    """
    Permet l'accès uniquement au propriétaire du profil ou à un superuser.
    """
    def has_object_permission(self, request, view, obj):
        # Le superuser a tous les droits
        if request.user.is_superuser:
            return True
        # Sinon, l'objet (le profil) doit appartenir à l'utilisateur connecté
        return obj == request.user


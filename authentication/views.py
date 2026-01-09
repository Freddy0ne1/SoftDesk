from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .models import User
from .serializers import UserSerializer
from .permissions import IsOwnerOrSuperUser

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des Utilisateurs.
    Gère l'inscription (Create), l'affichage de la liste (List) et la gestion de profil (Retrieve, Update, Destroy).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Définit les permissions de manière dynamique selon l'action demandée par le client.
        """
        if self.action == "create":
            # Cas de l'inscription :
            # On doit autoriser n'importe qui (anonyme) à créer un compte.
            permission_classes = [AllowAny]

        elif self.action == "list":
            # Cas de la liste globale des utilisateurs :
            # Pour des raisons de confidentialité, seul un administrateur peut voir tout le monde.
            permission_classes = [IsAuthenticated, IsAdminUser]

        elif self.action in ["retrieve", "update", "partial_update", "destroy"]:
            # Cas de la consultation ou modification de profil :
            # L'utilisateur doit être connecté ET être le propriétaire du compte (ou un superuser).
            permission_classes = [IsAuthenticated, IsOwnerOrSuperUser]

        else:
            # Sécurité par défaut pour toute autre action non prévue :
            # On exige au minimum que l'utilisateur soit authentifié.
            permission_classes = [IsAuthenticated]

        # On instancie et retourne la liste des permissions
        return [permission() for permission in permission_classes]
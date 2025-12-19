from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .models import User
from .serializers import UserSerializer
from .permissions import IsOwnerOrSuperUser

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    def get_permissions(self):
        """
        Définit les permissions selon l'action demandée.
        """
        if self.action == "create":
            # L'inscription est ouverte à tous (même non connectés)
            permission_classes = [AllowAny]

        elif self.action == "list":
            # Seul le superuser/admin peut voir la liste complète des utilisateurs
            permission_classes = [IsAuthenticated, IsAdminUser]

        elif self.action in ["retrieve", "update", "partial_update", "destroy"]:
            # Seul le propriétaire du profil ou le superuser/admin peut accéder à ces actions
            permission_classes = [IsAuthenticated, IsOwnerOrSuperUser]

        else:
            # Par défaut, on sécurise l'accès
            permission_classes = [IsAuthenticated]

        # On applique les permissions           
        return [permission() for permission in permission_classes]
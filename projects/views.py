from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Project, Contributor, Issue, Comment
from .serializers import (
    ProjectListSerializer,
    ProjectRetrieveSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)

# On importe uniquement les permissions pertinentes pour les projets
from .permissions import IsAuthorOrReadOnly, IsProjectContributor


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Gestion des projets.
    """

    queryset = Project.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return ProjectRetrieveSerializer

    def get_permissions(self):
        """
        Définit les permissions selon l'action.
        """
        if self.action == "list":
            # Liste : Juste être connecté suffit
            permission_classes = [IsAuthenticated]
        else:
            # Détail/Modif : Il faut être Contributeur (pour voir) OU Auteur (pour modifier)
            # On a retiré IsOwnerOrSuperUser qui bloquait tout le monde sauf l'admin
            permission_classes = [
                IsAuthenticated,
                IsProjectContributor,
                IsAuthorOrReadOnly,
            ]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = self.request.user
        project = serializer.save(author=user)
        Contributor.objects.create(user=user, project=project)


class ContributorViewSet(viewsets.ModelViewSet):
    """
    Gestion des contributeurs.
    """

    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    # Ici, on garde IsProjectContributor pour vérifier que l'admin du projet a le droit d'agir
    # Attention : pour la suppression, il faudra vérifier que c'est bien l'auteur du projet qui agit.
    # Pour l'instant, on laisse simple.
    permission_classes = [IsAuthenticated, IsProjectContributor]


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    # CORRECTION : On utilise IsAuthorOrReadOnly au lieu de IsOwnerOrSuperUser
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # CORRECTION : Idem ici
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectListSerializer, ProjectRetrieveSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly, IsProjectContributor
from authentication.permissions import IsOwnerOrSuperUser


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Gestion des projets (Création, Lecture, Modification, Suppression).
    """
    # 1. Par défaut, on affiche tous les projets
    queryset = Project.objects.all()

    def get_serializer_class(self):
        """
        Choisit le serializer selon l'action.
        - Si on demande la liste ("list") : on utilise ProjectListSerializer
        - Sinon : on utilise ProjectRetrieveSerializer
        """
        if self.action == "list":
            return ProjectListSerializer
        return ProjectRetrieveSerializer

    def get_permissions(self):
        """
        Définit les permissions selon l'action.
        - Liste : Juste être connecté suffit (IsAuthenticated).
        - Détail /Modif : Il faut être auteur ou contributeur du projet.
        """
        if self.action == "list":
            # Tout le monde (connecté) peut voir la liste
            permission_classes = [IsAuthenticated]
        else:
            # Pour voir le détail (/projects/1/), il faut être contributeur
            permission_classes = [IsAuthenticated, IsProjectContributor, IsOwnerOrSuperUser]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = self.request.user
        # Cette méthode permet d'assigner automatiquement l'auteur du projet
        # à l'utilisateur qui envoie la requête (request.user)
        project = serializer.save(author=user)
        # On ajoute automatiquement l'auteur comme contributeur
        Contributor.objects.create(user=user, project=project)


class ContributorViewSet(viewsets.ModelViewSet):
    """
    Gestion des contributeurs d'un projet.
    """
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsOwnerOrSuperUser, IsProjectContributor]

class IssueViewSet(viewsets.ModelViewSet):
    
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsOwnerOrSuperUser, IsProjectContributor, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        # L'auteur est automatiquement l'utilisateur connecté
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrSuperUser, IsProjectContributor, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Gestion des projets (Création, Lecture, Modification, Suppression).
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

class IssueViewSet(viewsets.ModelViewSet):
    
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # L'auteur est automatiquement l'utilisateur connecté
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
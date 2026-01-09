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

# Import des permissions personnalisées :
# - IsAuthorOrReadOnly : Seul l'auteur peut modifier/supprimer.
# - IsProjectContributor : Il faut être membre du projet pour voir son contenu.
# - IsProjectAuthor : Spécifique pour gérer (ajouter/supprimer) les contributeurs.
from .permissions import IsAuthorOrReadOnly, IsProjectContributor, IsProjectAuthor


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des Projets (CRUD).
    Permet de lister, créer, récupérer, mettre à jour et supprimer des projets.
    """

    queryset = Project.objects.all()

    def get_serializer_class(self):
        """
        Définit le sérialiseur à utiliser selon l'action demandée.
        """
        # Si on demande la liste globale, on utilise le sérialiseur "léger" (ID + Nom)
        if self.action == "list":
            return ProjectListSerializer
        
        # Pour le détail, la création ou la modification, on utilise le sérialiseur complet
        return ProjectRetrieveSerializer

    def get_permissions(self):
        """
        Définit les permissions de manière dynamique selon l'action.
        """
        if self.action == "list":
            # La liste des projets est visible pour tout utilisateur connecté
            permission_classes = [IsAuthenticated]
        else:
            # Pour accéder au détail, modifier ou supprimer :
            # 1. Il faut être connecté.
            # 2. Il faut être contributeur (ou auteur) pour VOIR.
            # 3. Il faut être l'auteur pour MODIFIER ou SUPPRIMER.
            permission_classes = [
                IsAuthenticated,
                IsProjectContributor,
                IsAuthorOrReadOnly,
            ]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        Personnalise la sauvegarde lors de la création d'un projet.
        """
        user = self.request.user
        
        # 1. On sauvegarde le projet en définissant l'utilisateur connecté comme auteur
        project = serializer.save(author=user)
        
        # 2. Logique métier : L'auteur est automatiquement ajouté comme contributeur
        Contributor.objects.create(user=user, project=project)


class ContributorViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des Contributeurs (membres d'un projet).
    Attention : La sécurité est critique ici pour empêcher les invitations non autorisées.
    """

    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

    # Permissions strictes :
    # - IsProjectContributor : Pour voir la liste des membres.
    # - IsProjectAuthor : CRUCIAL pour empêcher n'importe qui d'ajouter (POST) 
    #   ou supprimer (DELETE) un membre sur un projet qui ne lui appartient pas.
    permission_classes = [IsAuthenticated, IsProjectContributor, IsProjectAuthor]


class IssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des Problèmes (Issues).
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    
    # Tout contributeur peut voir/créer, seul l'auteur de l'issue peut la modifier.
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        """
        Lors de la création, l'auteur est automatiquement rempli avec l'utilisateur connecté.
        """
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des Commentaires liés aux Issues.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    # Tout contributeur peut voir/commenter, seul l'auteur du commentaire peut le modifier.
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        """
        Lors de la création, l'auteur est automatiquement rempli avec l'utilisateur connecté.
        """
        serializer.save(author=self.request.user)
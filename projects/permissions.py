from rest_framework.permissions import BasePermission, SAFE_METHODS
from projects.models import Project


class IsAuthorOrReadOnly(BasePermission):
    """
    Règle :
    - Tout le monde (authentifié) peut LIRE (GET, HEAD, OPTIONS).
    - Seul l'AUTEUR peut MODIFIER ou SUPPRIMER (PUT, DELETE).
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class IsProjectContributor(BasePermission):
    """
    Règle :
    - L'utilisateur doit être contributeur du projet OU l'auteur pour accéder à la ressource.
    """

    def has_object_permission(self, request, view, obj):
        # 1. Récupération du projet parent
        if isinstance(obj, Project):
            project = obj
        elif hasattr(obj, "project"):
            project = obj.project
        elif hasattr(obj, "issue"):
            project = obj.issue.project
        else:
            return False

        # 2. Vérifications
        # Grâce à related_name='contributors', cette ligne fonctionne parfaitement :
        is_contributor = project.contributors.filter(user=request.user).exists()

        # On n'oublie pas le chef de projet !
        is_author = project.author == request.user

        return is_contributor or is_author


class IsProjectAuthor(BasePermission):
    """
    Permission spécifique pour la gestion des contributeurs.
    Seul l'auteur du projet peut AJOUTER ou SUPPRIMER des membres.
    """

    def has_permission(self, request, view):
        # Cette méthode sécurise le POST (l'ajout d'un contributeur)
        if request.method == "POST":
            # 1. On récupère le nom du projet envoyé dans le JSON
            project_name = request.data.get("project")

            if not project_name:
                return False  # Pas de projet spécifié = Rejet

            try:
                # 2. On cherche le projet dans la base
                project = Project.objects.get(name=project_name)

                # 3. On vérifie : Est-ce que c'est bien le chef qui demande ?
                return project.author == request.user

            # Le projet n'existe pas
            except Project.DoesNotExist:
                return False

        # Pour les autres méthodes (GET, DELETE), on laisse passer ici,
        # la vérification se fera dans has_object_permission
        return True

    def has_object_permission(self, request, view, obj):
        # Cette méthode sécurise le DELETE (supprimer un contributeur)
        if request.method == "DELETE":
            # 'obj' est ici l'objet Contributor
            # On vérifie que l'utilisateur est l'auteur du projet lié
            return obj.project.author == request.user

        return True

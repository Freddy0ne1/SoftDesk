from rest_framework.permissions import BasePermission, SAFE_METHODS
from projects.models import Project


class IsAuthorOrReadOnly(BasePermission):
    """
    Permission permettant de restreindre les modifications à l'auteur de l'objet.
    
    Règles :
    - Méthodes de lecture (GET, HEAD, OPTIONS) : Autorisées pour tout utilisateur authentifié.
    - Méthodes d'écriture (PUT, PATCH, DELETE) : Autorisées uniquement si l'utilisateur est l'auteur.
    """

    def has_object_permission(self, request, view, obj):
        # 1. Si la méthode est "sûre" (lecture seule), on autorise l'accès.
        if request.method in SAFE_METHODS:
            return True
        
        # 2. Sinon (modification/suppression), on vérifie que l'utilisateur est bien l'auteur.
        return obj.author == request.user


class IsProjectContributor(BasePermission):
    """
    Permission vérifiant l'appartenance à un projet.
    
    Cette classe remonte la hiérarchie des objets (Commentaire -> Issue -> Projet)
    pour s'assurer que l'utilisateur a le droit de voir ou d'interagir avec la ressource.
    
    Règles :
    - L'utilisateur doit être dans la liste des contributeurs.
    - OU l'utilisateur doit être l'auteur du projet (admin).
    """

    def has_object_permission(self, request, view, obj):
        # 1. Identification du projet parent selon le type d'objet actuel
        if isinstance(obj, Project):
            # L'objet est le projet lui-même
            project = obj
        elif hasattr(obj, "project"):
            # L'objet est une Issue (liée directement à un projet)
            project = obj.project
        elif hasattr(obj, "issue"):
            # L'objet est un Commentaire (lié à une issue, elle-même liée à un projet)
            project = obj.issue.project
        else:
            # Sécurité : Si on ne peut pas relier l'objet à un projet, on bloque par défaut.
            return False

        # 2. Vérification des droits d'accès
        
        # Vérifie si l'utilisateur est présent dans la table de liaison 'contributors'
        # (Nécessite related_name='contributors' dans le modèle Contributor)
        is_contributor = project.contributors.filter(user=request.user).exists()

        # Vérifie si l'utilisateur est le créateur du projet (qui a implicitement tous les droits)
        is_author = project.author == request.user

        # L'accès est validé si l'une des deux conditions est vraie
        return is_contributor or is_author


class IsProjectAuthor(BasePermission):
    """
    Permission administrative spécifique à la gestion des contributeurs (ContributorViewSet).
    
    Objectif :
    Empêcher un simple contributeur d'inviter ou d'exclure des gens.
    Seul le propriétaire du projet (Auteur) a ce pouvoir.
    """

    def has_permission(self, request, view):
        """
        Vérification globale pour l'ajout (POST).
        Comme l'objet Contributor n'existe pas encore, on doit analyser les données envoyées (request.data).
        """
        if request.method == "POST":
            # 1. Récupération du nom du projet ciblé dans le corps de la requête
            project_name = request.data.get("project")

            if not project_name:
                return False  # Rejet immédiat si le projet n'est pas spécifié

            try:
                # 2. Recherche du projet en base de données via son nom (Slug)
                project = Project.objects.get(name=project_name)

                # 3. Vérification : L'utilisateur connecté est-il le propriétaire de ce projet ?
                return project.author == request.user

            except Project.DoesNotExist:
                # Le projet indiqué n'existe pas, on refuse l'accès
                return False

        # Pour les autres méthodes (GET, DELETE, etc.), on laisse passer cette étape.
        # La vérification se fera au niveau de l'objet (has_object_permission).
        return True

    def has_object_permission(self, request, view, obj):
        """
        Vérification au niveau de l'objet pour la suppression (DELETE).
        """
        if request.method == "DELETE":
            # 'obj' correspond ici à l'instance de Contributor (le lien utilisateur-projet).
            # On vérifie que celui qui demande la suppression est bien l'auteur du projet concerné.
            return obj.project.author == request.user

        # Les autres méthodes (comme GET) sont gérées par d'autres permissions (ex: IsProjectContributor).
        return True
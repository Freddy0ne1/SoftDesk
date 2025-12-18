from rest_framework.permissions import BasePermission, SAFE_METHODS
from projects.models import Project

class IsAuthorOrReadOnly(BasePermission):
    """
    Règle : 
    - Tout le monde (authentifié) peut LIRE (GET, HEAD, OPTIONS).
    - Seul l'AUTEUR peut MODIFIER ou SUPPRIMER (PUT, DELETE).
    """
    def has_object_permission(self, request, view, obj):
        # Si c'est une méthode de lecture, on autorise
        if request.method in SAFE_METHODS:
            return True
        
        # Sinon (modification), on vérifie que c'est bien l'auteur
        return obj.author == request.user


class IsProjectContributor(BasePermission):
    """
    Règle :
    - L'utilisateur doit être contributeur du projet pour accéder à la ressource.
    """

    def has_object_permission(self, request, view, obj):
        # 1. On trouve d'abord quel est le projet concerné
        
        # Si l'objet est directement un Projet
        if isinstance(obj, Project):
            project = obj

        # Si l'objet est une Issue (il a un attribut "project")
        elif hasattr(obj, "project"):
            project = obj.project

        # Si l'objet est un Commentaire (il a un attribut "issue" qui a un attribut "project")
        elif hasattr(obj, "issue"):
            project = obj.issue.project

        # Si on n'arrive pas à trouver de projet, par sécurité, on bloque
        else:
            return False

        # 2. On vérifie si l'utilisateur est dans la liste des contributeurs de ce projet
        return project.contributors.filter(user=request.user).exists()
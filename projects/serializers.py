from rest_framework import serializers
from authentication.models import User
from .models import Project, Contributor, Issue, Comment

# Constante pour uniformiser le format des dates dans toute l'API
# read_only=True : La date est gérée automatiquement par Django (auto_now_add), on ne l'envoie jamais manuellement.
CREATE_TIME = serializers.DateTimeField(format="%d-%m-%Y %H:%M", read_only=True)


class ProjectRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer complet pour l'affichage détaillé, la modification et la suppression d'un projet.
    """
    
    # source='author.username' : On va chercher l'attribut 'username' de l'objet 'author'.
    # Cela permet d'afficher "Alice" au lieu de l'ID "42".
    author = serializers.ReadOnlyField(source="author.username")

    # On applique le format de date personnalisé
    created_time = CREATE_TIME

    class Meta:
        model = Project
        fields = ["id", "name", "description", "type", "author", "created_time"]
        # On protège created_time en lecture seule explicitement ici aussi
        read_only_fields = ["created_time"]


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Serializer allégé pour la liste des projets.
    Optimise les performances en ne renvoyant que les infos essentielles.
    """
    
    class Meta:
        model = Project
        fields = ["id", "name", "type"]


class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer pour gérer les membres (Contributeurs) d'un projet.
    Transforme les pseudos (Text) en objets User (Database) et vice-versa.
    """

    # SlugRelatedField : Permet d'utiliser le 'username' dans le JSON 
    # au lieu de devoir connaître l'ID de l'utilisateur.
    # queryset=User.objects.all() : Indispensable pour que Django puisse retrouver l'user "Toto" en base.
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username"
    )
    
    created_time = CREATE_TIME
    
    # Idem pour le projet : on peut l'identifier par son nom unique.
    project = serializers.SlugRelatedField(
        queryset=Project.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = Contributor
        fields = ["id", "user", "project", "created_time"]
        read_only_fields = ["created_time"]


class IssueSerializer(serializers.ModelSerializer):
    """
    Serializer pour les Problèmes (Issues).
    Contient une validation complexe pour vérifier l'assignation.
    """

    # Affichage du nom de l'auteur (Lecture seule)
    author = serializers.ReadOnlyField(source="author.username")
    
    # L'assigné est choisi via son pseudo.
    # required=False : Une issue peut n'être assignée à personne au début.
    assignee = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username",
        required=False 
    )
    
    created_time = CREATE_TIME
    
    # Le projet est choisi via son nom.
    project = serializers.SlugRelatedField(
        queryset=Project.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = Issue
        fields = [
            "id", "title", "description", "tag", "priority", 
            "status", "project", "author", "assignee", "created_time"
        ]
        read_only_fields = ["author", "created_time"]

    def validate(self, data):
        """
        Validation personnalisée (niveau Objet).
        Règle métier : On ne peut assigner une tâche qu'à un membre du projet.
        """
        # 1. On récupère les données entrantes (converties en objets par les SlugFields)
        project = data.get('project')
        assignee = data.get('assignee')

        # Cas particulier du PATCH (mise à jour partielle) :
        # Si le projet n'est pas dans les données envoyées, on récupère celui de l'issue existante.
        if self.instance and not project:
            project = self.instance.project

        # 2. Si un assigné est défini, on lance l'enquête de sécurité
        if assignee:
            # Vérif A : Est-ce un contributeur officiel ?
            is_contributor = Contributor.objects.filter(user=assignee, project=project).exists()
            
            # Vérif B : Est-ce l'auteur du projet (le chef) ?
            is_author = (project.author == assignee)

            # Si ce n'est ni l'un ni l'autre => ERREUR
            if not is_contributor and not is_author:
                raise serializers.ValidationError(
                    {"assignee": f"L'utilisateur '{assignee.username}' ne fait pas partie du projet '{project.name}'."}
                )

        return data


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer pour les Commentaires.
    """
    
    # Auteur en lecture seule (pseudo)
    author = serializers.ReadOnlyField(source="author.username")
    
    created_time = CREATE_TIME
    

    class Meta:
        model = Comment
        fields = ["uuid", "description", "issue", "author", "created_time"]
        read_only_fields = ["author", "uuid", "created_time"]
from authentication.models import User
from .models import Project, Contributor, Issue, Comment
from rest_framework import serializers


CREATE_TIME = serializers.DateTimeField(format="%d-%m-%Y %H:%M", read_only=True)

class ProjectSerializer(serializers.ModelSerializer):
    # On redéfinit le champ author.
    # source='author.username' permet d'aller chercher le pseudo de l'utilisateur lié.
    # ReadOnlyField assure que ce champ ne sert qu'à l'affichage (on ne peut pas le modifier directement).
    author = serializers.ReadOnlyField(source="author.username")

    # On force le format Jour-Mois-Année Heure:Minute
    #created_time = CREATE_TIME

    class Meta:
        model = Project
        fields = ["id", "name", "description", "type", "author", "created_time"]
        # Note : 'author' est déjà en lecture seule grâce à la ligne au-dessus, 
        # mais on laisse created_time ici.
        read_only_fields = ["created_time"]


class ContributorSerializer(serializers.ModelSerializer):
    # SlugRelatedField permet d'utiliser le 'username' au lieu de l'ID
    # queryset=... est nécessaire pour que l'API puisse retrouver l'utilisateur quand on lui envoie un pseudo
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username"
    )
    
    # On force le format Jour-Mois-Année Heure:Minute
    #created_time = CREATE_TIME
    
    # On peut faire pareil pour le projet si tu veux voir son nom au lieu de son ID
    project = serializers.SlugRelatedField(
        queryset=Project.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = Contributor
        fields = ["id", "user", "project", "created_time"]
        read_only_fields = ["created_time"]


class IssueSerializer(serializers.ModelSerializer):
    # On affiche les noms au lieu des ID pour la lisibilité
    author = serializers.ReadOnlyField(source="author.username")
    
    # Pour l'assigné, on veut pouvoir choisir via le pseudo (Lecture et Écriture)
    assignee = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username",
        required=False # Ce champ n'est pas obligatoire
    )
    
    # On force le format Jour-Mois-Année Heure:Minute
    #created_time = CREATE_TIME
    
    # Pour le projet, on choisit via son nom exact (ou tu peux laisser l'ID par défaut si tu préfères)
    project = serializers.SlugRelatedField(
        queryset=Project.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = Issue
        fields = ["id", "title", "description", "tag", "priority", "status", "project", "author", "assignee", "created_time"]
        read_only_fields = ["author", "created_time"]

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    
    # On force le format Jour-Mois-Année Heure:Minute
    #created_time = CREATE_TIME
    
    # Pour lier à l'issue, on utilise son ID (par défaut) car les titres peuvent être longs ou en doublon
    # Mais on peut afficher le titre si tu veux (via un SerializerMethodField), restons simple pour l'instant.

    class Meta:
        model = Comment
        fields = ["uuid", "description", "issue", "author", "created_time"]
        read_only_fields = ["author", "uuid", "created_time"]
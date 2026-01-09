from django.db import models
from django.conf import settings
import uuid


class Project(models.Model):
    """
    Modèle représentant un projet.
    C'est l'entité principale qui contient des tâches (Issues) et possède des membres (Contributeurs).
    """
    
    # Choix restreints pour le type de plateforme.
    # Format : (Valeur en base de données, Valeur affichée à l'utilisateur)
    TYPE_CHOICES = [
        ('back-end', 'Back-end'),
        ('front-end', 'Front-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    ]

    # L'auteur est le propriétaire du projet.
    # settings.AUTH_USER_MODEL est la bonne pratique pour référencer le User (plutôt que d'importer la classe).
    # related_name='owned_projects' permet de faire : user.owned_projects.all()
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='owned_projects'
    )
    
    # unique=True empêche d'avoir deux projets avec exactement le même nom.
    name = models.CharField(max_length=128, unique=True, verbose_name="Nom du projet")
    description = models.TextField(max_length=2048, blank=True, verbose_name="Description")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type de projet")
    
    # auto_now_add=True fige la date lors de la création initiale (non modifiable par la suite).
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def __str__(self):
        return self.name


class Contributor(models.Model):
    """
    Table de liaison explicite entre Utilisateur et Projet.
    Si un utilisateur est présent dans cette table pour un projet donné, il a des droits d'accès.
    """
    
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='contributions'
    )
    
    # related_name='contributors' est CRUCIAL ici car il est utilisé dans mes permissions (IsProjectContributor).
    project = models.ForeignKey(
        to=Project, 
        on_delete=models.CASCADE, 
        related_name='contributors'
    )
    
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")

    class Meta:
        # Contrainte d'unicité composée :
        # Empêche d'ajouter le même utilisateur deux fois au même projet.
        unique_together = ('user', 'project')
        verbose_name = "Contributeur"

    def __str__(self):
        return f"{self.user} contribue à {self.project}"


class Issue(models.Model):
    """
    Modèle représentant un problème, un ticket ou une tâche à réaliser dans le cadre d'un projet.
    """
    
    # Listes de choix pour standardiser les statuts et priorités
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')]
    TAG_CHOICES = [('BUG', 'Bug'), ('FEATURE', 'Feature'), ('TASK', 'Task')]
    STATUS_CHOICES = [('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Finished', 'Finished')]

    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(max_length=2048, verbose_name="Description")
    tag = models.CharField(max_length=30, choices=TAG_CHOICES, verbose_name="Balise")
    priority = models.CharField(max_length=30, choices=PRIORITY_CHOICES, verbose_name="Priorité")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='To Do', verbose_name="Statut")
    
    # -- Relations --
    
    # Si le projet est supprimé, ses tickets le sont aussi.
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='issues')
    
    # Auteur du ticket (celui qui a signalé le bug).
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issues_created')
    
    # Responsable du ticket (Assignee).
    # on_delete=models.SET_NULL : Si le responsable quitte l'entreprise (User supprimé),
    # le ticket reste mais le champ assignee devient vide (null).
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_issues'
    )
    
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Modèle représentant un commentaire ajouté sur une Issue.
    Identifié techniquement par un UUID pour éviter l'énumération simple des IDs.
    """
    
    # UUIDField génère un identifiant unique universel (ex: 123e4567-e89b-12d3-a456-426614174000).
    # editable=False empêche de modifier cet ID via l'admin ou les formulaires.
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    description = models.TextField(max_length=2048, verbose_name="Commentaire")
    
    # -- Relations --
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.author} sur {self.issue}"
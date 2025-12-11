from django.db import models
from django.conf import settings
import uuid


class Project(models.Model):
    """
    Modèle représentant un projet.
    Un projet a un auteur (le créateur) et plusieurs contributeurs.
    """
    # Liste de choix pour le type de projet (Valeur stockée, Valeur affichée)
    TYPE_CHOICES = [
        ('back-end', 'Back-end'),
        ('front-end', 'Front-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    ]

    # L'auteur est lié à un utilisateur. Si l'utilisateur est supprimé, ses projets le sont aussi (CASCADE).
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_projects')
    name = models.CharField(max_length=128, unique=True, verbose_name="Nom du projet")
    description = models.TextField(max_length=2048, blank=True, verbose_name="Description")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type de projet")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def __str__(self):
        return self.name

class Contributor(models.Model):
    """
    Table de liaison entre un Utilisateur et un Projet.
    Définit qui a le droit d'accéder au projet.
    """
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contributions')
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='contributors')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")

    class Meta:
        # Empêche d'ajouter deux fois le même utilisateur au même projet
        unique_together = ('user', 'project')
        verbose_name = "Contributeur"

    def __str__(self):
        return f"{self.user} contribue à {self.project}"


class Issue(models.Model):
    """
    Modèle représentant un problème (ou tâche) lié à un projet.
    """
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')]
    TAG_CHOICES = [('BUG', 'Bug'), ('FEATURE', 'Feature'), ('TASK', 'Task')]
    STATUS_CHOICES = [('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Finished', 'Finished')]

    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(max_length=2048, verbose_name="Description")
    tag = models.CharField(max_length=30, choices=TAG_CHOICES, verbose_name="Balise")
    priority = models.CharField(max_length=30, choices=PRIORITY_CHOICES, verbose_name="Priorité")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='To Do', verbose_name="Statut")
    
    # Liens
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='issues')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issues_created')
    # L'assigné est optionnel (null=True) car une tâche peut ne pas être encore attribuée
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')
    
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    """
    Modèle représentant un commentaire sur une issue.
    Identifié par un UUID unique.
    """
    # uuid4 génère une suite de caractères aléatoires uniques (ex: a0eebc99-9c0b...)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField(max_length=2048, verbose_name="Commentaire")
    
    # Liens
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.author} sur {self.issue}"
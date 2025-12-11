from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    can_be_contacted = models.BooleanField(default=False, verbose_name="Peut être contacté")
    can_data_be_shared = models.BooleanField(default=False, verbose_name="Données partageables")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def __str__(self):
        return self.username
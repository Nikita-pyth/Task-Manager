from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Team(models.Model):
    name = models.CharField(max_length=100)
    admins = models.ManyToManyField(User, related_name="managed_teams")

    def __str__(self):
        return self.name
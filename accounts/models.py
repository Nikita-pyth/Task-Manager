from django.contrib.auth.models import AbstractUser
from django.db import models

from positions.models import Position
from teams.models import Team


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="workers", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

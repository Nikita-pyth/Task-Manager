from django.db import models

from teams.models import Team


class Project(models.Model):
    name = models.CharField(max_length=200)
    teams = models.ManyToManyField(Team, related_name="projects")

    def __str__(self):
        return self.name

from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey("Position", on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey("Team", on_delete=models.CASCADE, related_name="workers", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class Project(models.Model):
    name = models.CharField(max_length=200)
    teams = models.ManyToManyField(Team, related_name="projects")

    def __str__(self):
        return self.name


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    name = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    type = models.ForeignKey("TaskType", on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="tasks", null=True, blank=True)
    assignees = models.ManyToManyField("Worker", related_name="tasks")
    tags = models.ManyToManyField("Tag", blank=True)

    def __str__(self):
        return self.name
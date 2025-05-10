from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import Task, Tag, TaskType
from projects.models import Project
from teams.models import Team

User = get_user_model()


class TaskViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="pass")
        self.client.login(username="user1", password="pass")

    def test_task_create_assigns_user(self):
        response = self.client.post(reverse("tasks:create"), {
            "name": "New Task",
            "description": "Desc",
            "priority": "medium",
            "is_completed": False,
        })
        task = Task.objects.first()
        self.assertIn(self.user, task.assignees.all())
        self.assertRedirects(response, reverse("tasks:index"))

    def test_task_list_view_filters_and_splits_tasks(self):
        personal = Task.objects.create(name="Solo", description="...", project=None)
        personal.assignees.add(self.user)

        team = Team.objects.create(name="Test Team")
        project = Project.objects.create(name="Proj X")
        project.teams.add(team)
        project_task = Task.objects.create(name="Group", description="...", project=project)
        project_task.assignees.add(self.user)

        response = self.client.get(reverse("tasks:index"))
        self.assertIn(personal, response.context["personal_tasks"])
        self.assertIn(project_task, response.context["project_tasks"])

    def test_task_status_toggle(self):
        task = Task.objects.create(name="To Toggle", description="...", is_completed=False)
        task.assignees.add(self.user)

        self.client.post(reverse("tasks:toggle-status", kwargs={"pk": task.pk}))
        task.refresh_from_db()
        self.assertTrue(task.is_completed)

    def test_task_status_toggle_ignores_non_assignee(self):
        other_user = User.objects.create_user(username="outsider", password="pass")
        task = Task.objects.create(name="Forbidden", description="...")
        task.assignees.add(other_user)

        self.client.post(reverse("tasks:toggle-status", kwargs={"pk": task.pk}))
        task.refresh_from_db()
        self.assertFalse(task.is_completed)  # no change

    def test_tag_create_redirects_to_next_if_safe(self):
        response = self.client.post(
            reverse("tasks:tag-create") + "?next=" + reverse("tasks:index"),
            {"name": "QuickTag"}
        )
        self.assertRedirects(response, reverse("tasks:index"))

    def test_tag_create_redirects_to_default_if_no_next(self):
        response = self.client.post(reverse("tasks:tag-create"), {"name": "FallbackTag"})
        self.assertRedirects(response, reverse("tasks:index"))

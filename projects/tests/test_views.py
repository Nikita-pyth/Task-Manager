from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from projects.models import Project
from teams.models import Team
from accounts.models import Worker
from tasks.models import Task

User = get_user_model()


class ProjectViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="pass")
        self.other_user = User.objects.create_user(username="notadmin", password="pass")

        self.team = Team.objects.create(name="A-Team")
        self.team.admins.add(self.user)

        self.project = Project.objects.create(name="Project X")
        self.project.teams.add(self.team)

    def test_detail_view_admin_projects_context(self):
        self.client.login(username="admin", password="pass")
        url = reverse("projects:detail", kwargs={"pk": self.project.pk})
        response = self.client.get(url)

        admin_projects = response.context["admin_projects"]
        self.assertIn(self.project, admin_projects)

    def test_create_view_passes_user_to_form(self):
        self.client.login(username="admin", password="pass")
        url = reverse("projects:create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("teams", response.context["form"].fields)
        self.assertQuerySetEqual(
            response.context["form"].fields["teams"].queryset,
            Team.objects.filter(admins=self.user),
            transform=lambda x: x
        )

    def test_update_view_forbidden_for_non_admin(self):
        self.client.login(username="notadmin", password="pass")
        url = reverse("projects:update", kwargs={"pk": self.project.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_project_task_create_forbidden_for_non_admin_team(self):
        self.client.login(username="notadmin", password="pass")
        url = reverse("projects:create-task", kwargs={"pk": self.project.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_project_task_create_form_filters_assignees(self):
        worker1 = Worker.objects.create_user(username="teamworker", password="pass", team=self.team)
        self.client.login(username="admin", password="pass")

        url = reverse("projects:create-task", kwargs={"pk": self.project.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        assignees_qs = response.context["form"].fields["assignees"].queryset
        self.assertIn(worker1, assignees_qs)

from django.test import TestCase
from django.contrib.auth import get_user_model
from projects.forms import ProjectForm, ProjectScopedTaskForm
from teams.models import Team

Worker = get_user_model()


class ProjectFormTest(TestCase):
    def setUp(self):
        self.user = Worker.objects.create_user(username="adminuser", password="pass123")

    def test_teams_queryset_filtered_by_admin(self):
        team1 = Team.objects.create(name="Alpha")
        team2 = Team.objects.create(name="Beta")
        team1.admins.add(self.user)

        form = ProjectForm(user=self.user)

        self.assertIn(team1, form.fields["teams"].queryset)
        self.assertNotIn(team2, form.fields["teams"].queryset)

    def test_no_admin_teams_sets_empty_queryset_and_help_text(self):
        form = ProjectForm(user=self.user)
        self.assertEqual(form.fields["teams"].queryset.count(), 0)
        self.assertIn("You are not an admin in any team", form.fields["teams"].help_text)


class ProjectScopedTaskFormTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Alpha Team")
        self.member1 = Worker.objects.create_user(username="member1", password="123")
        self.member2 = Worker.objects.create_user(username="member2", password="123")
        self.member1.team = self.team
        self.member2.team = self.team
        self.member1.save()
        self.member2.save()

    def test_form_filters_assignees_to_team_members(self):
        form = ProjectScopedTaskForm(team_members=Worker.objects.filter(pk=self.member1.pk))
        assignee_qs = form.fields["assignees"].queryset

        self.assertIn(self.member1, assignee_qs)
        self.assertNotIn(self.member2, assignee_qs)

from django.test import TestCase
from projects.models import Project
from teams.models import Team


class ProjectModelTest(TestCase):

    def test_str_returns_project_name(self):
        project = Project.objects.create(name="Alpha Project")
        self.assertEqual(str(project), "Alpha Project")

    def test_can_add_teams_to_project(self):
        project = Project.objects.create(name="Beta Project")

        team1 = Team.objects.create(name="Team One")
        team2 = Team.objects.create(name="Team Two")

        project.teams.set([team1, team2])

        self.assertEqual(project.teams.count(), 2)
        self.assertIn(team1, project.teams.all())
        self.assertIn(team2, project.teams.all())

    def test_project_shows_up_in_team_projects(self):
        project = Project.objects.create(name="Gamma Project")
        team = Team.objects.create(name="Team Gamma")
        project.teams.add(team)

        self.assertIn(project, team.projects.all())

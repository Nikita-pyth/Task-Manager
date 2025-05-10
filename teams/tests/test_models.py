from django.test import TestCase
from django.contrib.auth import get_user_model
from teams.models import Team

User = get_user_model()

class TeamModelTest(TestCase):

    def test_str_returns_team_name(self):
        team = Team.objects.create(name="DevOps")
        self.assertEqual(str(team), "DevOps")

    def test_can_assign_admins_to_team(self):
        user1 = User.objects.create_user(username="admin1", password="pass")
        user2 = User.objects.create_user(username="admin2", password="pass")
        team = Team.objects.create(name="Engineering")
        team.admins.set([user1, user2])

        self.assertEqual(team.admins.count(), 2)
        self.assertIn(team, user1.managed_teams.all())
        self.assertIn(team, user1.managed_teams.all())
        self.assertIn(team, user2.managed_teams.all())


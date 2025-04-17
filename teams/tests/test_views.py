from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from teams.models import Team

User = get_user_model()

class TeamViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="pass")
        self.other_user = User.objects.create_user(username="user2", password="pass")
        self.client.login(username="user1", password="pass")

    def test_create_team_assigns_admin_and_worker(self):
        response = self.client.post(reverse("teams:create"), {
            "name": "Team Alpha"
        })

        team = Team.objects.first()
        self.assertEqual(team.name, "Team Alpha")
        self.assertIn(self.user, team.admins.all())
        self.assertIn(self.user, team.workers.all())
        self.assertRedirects(response, reverse("teams:list"))

        self.user.refresh_from_db()
        self.assertEqual(self.user.team, team)

    def test_update_team_forbidden_for_non_admin(self):
        team = Team.objects.create(name="Team Beta")
        team.admins.add(self.other_user)

        response = self.client.get(reverse("teams:update", kwargs={"pk": team.pk}))
        self.assertEqual(response.status_code, 403)

    def test_join_team_adds_user_to_workers(self):
        team = Team.objects.create(name="Team Gamma")

        response = self.client.post(reverse("teams:join", kwargs={"pk": team.pk}))
        self.assertRedirects(response, reverse("teams:detail", kwargs={"pk": team.pk}))
        self.assertIn(self.user, team.workers.all())

    def test_leave_team_removes_user_from_workers(self):
        team = Team.objects.create(name="Team Delta")
        team.workers.add(self.user)

        response = self.client.post(reverse("teams:leave", kwargs={"pk": team.pk}))
        self.assertRedirects(response, reverse("teams:detail", kwargs={"pk": team.pk}))
        self.assertNotIn(self.user, team.workers.all())

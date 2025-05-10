from django.test import TestCase
from django.contrib.auth import get_user_model
from positions.models import Position
from teams.models import Team

Worker = get_user_model()

class WorkerModelTest(TestCase):

    def test_str_representation_with_names(self):
        worker = Worker.objects.create(
            username="jsmith",
            first_name="John",
            last_name="Smith"
        )
        self.assertEqual(str(worker), "John Smith (jsmith)")

    def test_worker_can_have_position_and_team(self):
        position = Position.objects.create(name="Developer")
        team = Team.objects.create(name="Alpha")
        worker = Worker.objects.create_user(
            username="mdoe",
            password="secret",
            position=position,
            team=team
        )
        self.assertEqual(worker.position.name, "Developer")
        self.assertEqual(worker.team.name, "Alpha")

    def test_position_and_team_are_optional(self):
        worker = Worker.objects.create_user(username="noinfo", password="secret")
        self.assertIsNone(worker.position)
        self.assertIsNone(worker.team)

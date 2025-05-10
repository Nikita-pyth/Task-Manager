from django.test import TestCase
from positions.models import Position


class PositionModelTest(TestCase):

    def test_str_returns_name(self):
        position = Position.objects.create(name="Backend Developer")
        self.assertEqual(str(position), "Backend Developer")

    def test_can_create_position(self):
        position = Position.objects.create(name="Project Manager")
        self.assertEqual(Position.objects.count(), 1)
        self.assertEqual(position.name, "Project Manager")

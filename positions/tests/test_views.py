from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from positions.models import Position

Worker = get_user_model()

class PositionCreateViewTest(TestCase):

    def setUp(self):
        self.user = Worker.objects.create_user(username="testuser", password="testpass")
        self.url = reverse("positions:create")

    def test_position_create_redirects_to_user_update(self):
        self.client.login(username="testuser", password="testpass")

        response = self.client.post(self.url, {"name": "Designer"})

        position = Position.objects.first()
        self.assertEqual(position.name, "Designer")

        expected_redirect = reverse("accounts:update", kwargs={"pk": self.user.pk})
        self.assertRedirects(response, expected_redirect)

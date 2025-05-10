from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

Worker = get_user_model()

class WorkerViewTests(TestCase):
    def setUp(self):
        self.worker = Worker.objects.create_user(
            username="john",
            password="password123",
            first_name="John",
            last_name="Doe"
        )

    def test_create_view_redirects_to_login(self):
        response = self.client.post(reverse("accounts:create"), {
            "username": "newuser",
            "password1": "strongpassword123",
            "password2": "strongpassword123"
        })
        self.assertRedirects(response, reverse("accounts:login"))

    def test_login_redirects_to_detail(self):
        self.client.login(username="john", password="password123")
        response = self.client.post(reverse("accounts:login"), {
            "username": "john",
            "password": "password123"
        })
        self.assertRedirects(response, reverse("accounts:detail", kwargs={"pk": self.worker.pk}))

    def test_update_redirects_to_logged_user_detail(self):
        self.client.login(username="john", password="password123")
        response = self.client.post(reverse("accounts:update", kwargs={"pk": self.worker.pk}), {
            "first_name": "Johnny",
            "last_name": "Updated",
            "email": "johnny@example.com",
            "team": "",
            "position": ""
        })
        self.assertRedirects(response, reverse("accounts:detail", kwargs={"pk": self.worker.pk}))

    def test_delete_redirects_to_login(self):
        self.client.login(username="john", password="password123")
        response = self.client.post(reverse("accounts:delete", kwargs={"pk": self.worker.pk}))
        self.assertRedirects(response, reverse("accounts:login"))

    def test_detail_requires_login(self):
        response = self.client.get(reverse("accounts:detail", kwargs={"pk": self.worker.pk}))
        self.assertEqual(response.status_code, 302)

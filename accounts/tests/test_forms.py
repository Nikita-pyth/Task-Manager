from django.test import TestCase
from accounts.forms import WorkerCreationForm
from accounts.models import Worker


class WorkerCreationFormTest(TestCase):

    def test_form_valid_with_required_fields(self):
        form_data = {
            "username": "newworker",
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

        worker = form.save()
        self.assertIsInstance(worker, Worker)
        self.assertEqual(worker.username, "newworker")
        self.assertEqual(worker.email, "alice@example.com")

    def test_form_invalid_with_password_mismatch(self):
        form_data = {
            "username": "mismatch",
            "first_name": "Bob",
            "last_name": "Brown",
            "email": "bob@example.com",
            "password1": "Password123",
            "password2": "Different123",
        }
        form = WorkerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_form_missing_required_field(self):
        form_data = {
            "username": "incomplete",
            "password2": "Somepass123",
        }
        form = WorkerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)

    def test_form_meta_uses_worker_model(self):
        self.assertEqual(WorkerCreationForm._meta.model, Worker)
        self.assertEqual(
            WorkerCreationForm._meta.fields,
            ("username", "first_name", "last_name", "email")
        )

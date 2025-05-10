from django.test import TestCase
from django import forms
from tasks.forms import TaskForm
from tasks.models import TaskType, Tag, Task


class TaskFormTest(TestCase):

    def setUp(self):
        self.task_type = TaskType.objects.create(name="Bug")
        self.tag1 = Tag.objects.create(name="Urgent")
        self.tag2 = Tag.objects.create(name="Backend")

    def test_form_valid_with_minimal_required_fields(self):
        form_data = {
            "name": "Sample Task",
            "description": "Test description",
            "priority": Task.Priority.MEDIUM,
            "is_completed": False
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_name_and_description(self):
        form = TaskForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("description", form.errors)

    def test_form_saves_task_instance(self):
        form_data = {
            "name": "Real Task",
            "description": "Details",
            "priority": Task.Priority.HIGH,
            "is_completed": True
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
        task = form.save()
        self.assertEqual(task.name, "Real Task")
        self.assertTrue(task.is_completed)

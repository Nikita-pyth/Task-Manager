from django.test import TestCase
from django.contrib.auth import get_user_model
from tasks.models import Task, TaskType, Tag
from projects.models import Project

User = get_user_model()

class TaskModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="worker", password="pass")
        self.project = Project.objects.create(name="Test Project")
        self.task_type = TaskType.objects.create(name="Bug")
        self.tag = Tag.objects.create(name="Urgent")

    def test_str_returns_task_name(self):
        task = Task.objects.create(name="Fix login", description="Details...", project=self.project)
        self.assertEqual(str(task), "Fix login")

    def test_task_can_have_type_and_tag_and_assignees(self):
        task = Task.objects.create(
            name="Test",
            description="With full details",
            type=self.task_type,
            project=self.project
        )
        task.tags.add(self.tag)
        task.assignees.add(self.user)

        self.assertEqual(task.type.name, "Bug")
        self.assertIn(self.tag, task.tags.all())
        self.assertIn(self.user, task.assignees.all())

    def test_default_priority_is_medium(self):
        task = Task.objects.create(name="Priority test", description="Check default", project=self.project)
        self.assertEqual(task.priority, Task.Priority.MEDIUM)

    def test_ordering_by_completion_and_deadline(self):
        task1 = Task.objects.create(name="Done", description="X", is_completed=True, deadline="2025-05-01")
        task2 = Task.objects.create(name="Pending", description="Y", is_completed=False, deadline="2025-04-01")
        task3 = Task.objects.create(name="Pending Late", description="Z", is_completed=False, deadline="2025-04-10")

        tasks = list(Task.objects.all())
        self.assertEqual(tasks, [task2, task3, task1])

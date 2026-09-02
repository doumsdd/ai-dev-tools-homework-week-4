from django.test import TestCase, Client
from django.urls import reverse
from .models import Task


class TaskModelTest(TestCase):
    """Tests for the Task model."""

    def test_create_task(self):
        """Test creating a task."""
        task = Task.objects.create(title="Test task")
        self.assertEqual(task.title, "Test task")
        self.assertEqual(task.priority, "medium")
        self.assertFalse(task.completed)

    def test_create_task_with_priority(self):
        """Test creating a task with specific priority."""
        task = Task.objects.create(title="High priority", priority="high")
        self.assertEqual(task.priority, "high")

    def test_create_task_with_due_date(self):
        """Test creating a task with due date."""
        from datetime import date
        task = Task.objects.create(title="Task with due date", due_date=date(2026, 12, 31))
        self.assertEqual(task.due_date, date(2026, 12, 31))

    def test_task_str(self):
        """Test task string representation."""
        task = Task.objects.create(title="My task")
        self.assertEqual(str(task), "My task")

    def test_task_completion(self):
        """Test marking task as completed."""
        task = Task.objects.create(title="Task to complete")
        self.assertFalse(task.completed)
        self.assertIsNone(task.completed_at)


class TaskViewTest(TestCase):
    """Tests for task views."""

    def setUp(self):
        self.client = Client()
        self.task = Task.objects.create(
            title="Test task",
            priority="high",
        )

    def test_home_view(self):
        """Test home dashboard view."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_task_list_view(self):
        """Test task list view."""
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test task")

    def test_task_add_view_get(self):
        """Test task add form (GET)."""
        response = self.client.get(reverse('task_add'))
        self.assertEqual(response.status_code, 200)

    def test_task_add_view_post(self):
        """Test creating a task via POST."""
        response = self.client.post(reverse('task_add'), {
            'title': 'New task',
            'description': 'Description',
            'priority': 'high',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='New task').exists())

    def test_task_edit_view_get(self):
        """Test task edit form (GET)."""
        response = self.client.get(reverse('task_edit', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)

    def test_task_edit_view_post(self):
        """Test editing a task via POST."""
        response = self.client.post(reverse('task_edit', args=[self.task.pk]), {
            'title': 'Updated task',
            'priority': 'low',
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated task")
        self.assertEqual(self.task.priority, "low")

    def test_task_delete_view_get(self):
        """Test task delete confirmation (GET)."""
        response = self.client.get(reverse('task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)

    def test_task_delete_view_post(self):
        """Test deleting a task via POST."""
        response = self.client.post(reverse('task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_complete_view(self):
        """Test marking a task as completed."""
        response = self.client.get(reverse('task_complete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)


class PriorityTest(TestCase):
    """Tests for priority functionality."""

    def test_default_priority(self):
        """Test default priority is medium."""
        task = Task.objects.create(title="Default priority")
        self.assertEqual(task.priority, "medium")

    def test_high_priority(self):
        """Test high priority task."""
        task = Task.objects.create(title="High", priority="high")
        self.assertEqual(task.priority, "high")
        self.assertEqual(task.get_priority_display(), "High")

    def test_low_priority(self):
        """Test low priority task."""
        task = Task.objects.create(title="Low", priority="low")
        self.assertEqual(task.priority, "low")
        self.assertEqual(task.get_priority_display(), "Low")
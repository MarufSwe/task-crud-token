from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token
from ..views import TaskList
from ..models import Task


class TaskListTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username="test_user", password="test_password")
        self.token = Token.objects.create(user=self.user)

    def test_create_task_authenticated(self):
        # Test creating a task with a valid token
        task_data = {"title": "Test Task", "description": "Task description", "completed": False}
        request = self.factory.post('/api/tasks/', task_data, format='json',
                                    HTTP_AUTHORIZATION=f'Token {self.token.key}')
        view = TaskList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)  # HTTP 201 Created

        # Verify the task is created in the database
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.user, self.user)

    def test_create_task_unauthenticated(self):
        # Test attempting to create a task without a token (should fail)
        task_data = {"title": "Test Task", "description": "Task description", "completed": False}
        request = self.factory.post('/api/tasks/', task_data, format='json')
        view = TaskList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 401)  # HTTP 401 Unauthorized

        # Verify that no task is created in the database
        self.assertEqual(Task.objects.count(), 0)

    def test_list_tasks_authenticated(self):
        # Test listing tasks with a valid token
        Task.objects.create(title="Task 1", description="Description 1", completed=False, user=self.user)
        Task.objects.create(title="Task 2", description="Description 2", completed=True, user=self.user)

        request = self.factory.get('/api/tasks/', format='json', HTTP_AUTHORIZATION=f'Token {self.token.key}')
        view = TaskList.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)  # HTTP 200 OK
        self.assertEqual(len(response.data), 2)  # Expecting two tasks in the response

    def test_list_tasks_unauthenticated(self):
        # Test attempting to list tasks without a token (should fail)
        Task.objects.create(title="Task 1", description="Description 1", completed=False, user=self.user)
        Task.objects.create(title="Task 2", description="Description 2", completed=True, user=self.user)

        request = self.factory.get('/api/tasks/', format='json')
        view = TaskList.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 401)  # HTTP 401 Unauthorized


# for run this file: python manage.py test task_management.test.unit_test

from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from ..models import Task


class TaskModelTest(TestCase):
    def setUp(self) -> None:
        Task.objects.create(
            title="First Task", description='Complete Test Cases',
            due_date='2023-03-16', completed=False
        )
        Task.objects.create(
            title='Second Task', description="Learn Test Driven Dev",
            due_date='2023-03-15', completed=True
        )

    def test_title_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)

    def test_string_repr(self):
        task = Task.objects.get(id=1)
        self.assertEquals(str(task), 'First Task')
        task = Task.objects.get(id=2)
        self.assertEquals(str(task), 'Second Task')


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', email='tester@email.com', password='IUYDEYWH67382'
        )

    def test_create_user(self):
        self.assertEqual(self.user.username, 'tester')
        self.assertEqual(self.user.email, 'tester@email.com')
        self.assertTrue(self.user.check_password('IUYDEYWH67382'))

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@email.com',
            password='YGWJDHJW9823'
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)

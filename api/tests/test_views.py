import datetime
import json

from rest_framework.response import Response
from rest_framework.test import APITestCase
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from rest_framework import status
from django.contrib.auth.models import User, Group
from ..models import Task
from ..serializers import TaskSerializer, UserSerializer


class TaskViewSetTestCase(APITestCase):

    def setUp(self) -> None:
        self.task1 = Task.objects.create(
            title="First Task", description='Complete Test Cases',
            due_date='2023-03-16', completed=False
        )
        self.task2 = Task.objects.create(
            title='Second Task', description="Learn Test Driven Dev",
            due_date='2023-03-15', completed=True
        )
        self.user1 = User.objects.create_user(
            username='tester', email='tester@email.com', password='IUYDEYWH67382'
        )

    def test_all_tasks(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(
            reverse('task-list')
        )
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data, serializer.data
        )

    def test_create_test(self):
        data = {
            'title': 'Third Task',
            'description': 'Push to-do to repository',
            'due_date': '2023-03-12',
            'completed': False
        }
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(
            reverse('task-list'), data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Task.objects.all().count(), 3
        )

    def test_retrieve_task(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(
            reverse(
                'task-detail', args=[self.task1.id]
            )
        )
        task = Task.objects.get(id=self.task1.id)
        serializer = TaskSerializer(task)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data, serializer.data
        )

    def test_update_task(self):
        data = {
            'title': 'Update Second Task',
            'description': 'Test Driven Dev Learned',
            'due_date': '2023-03-12',
            'completed': True
        }
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(
            # url
            reverse(
                'task-detail', args=[self.task2.id]
            ),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task2.refresh_from_db()
        self.assertEqual(
            self.task2.title, 'Update Second Task'
        )
        self.assertEqual(
            self.task2.description, 'Test Driven Dev Learned'
        )
        self.assertEqual(
            self.task2.due_date, datetime.date(2023, 3, 12)
        )

    def test_delete_task(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(
            reverse(
                'task-detail',
                args=[self.task1.id]
            )
        )
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Task.objects.all().count(), 1
        )


class UserViewSetTestCase(APITestCase):
    # Changed djoser user_id_field to id from username in settings.py for this to work properly
    # Had to adjust fields in UserSerializer, so it can match with response data while testing
    def setUp(self):
        self.group1 = Group.objects.create(name='Group 1')
        self.group2 = Group.objects.create(name='Group 2')
        self.user1 = User.objects.create_user(
            username='tester1',
            email='tester1@email.com',
            password='IHBD089HJS'
        )
        self.user1.groups.add(self.group1)
        self.user2 = User.objects.create_user(
            username='tester2',
            email='tester2@email.com',
            password='HJDJW89903J'
        )
        self.user2.groups.add(self.group2)
        self.request = RequestFactory().get('/')
        self.request.user = self.user1

    def test_create_user(self):
        data = {
            'username': 'tester3',
            'email': 'tester3@email.com',
            'password': 'TYGSB789HJS'
        }
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(
            reverse('user-list'), data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            User.objects.all().count(), 3
        )

    def test_retrieve_user(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(
            reverse('user-detail', args=[self.user1.id])
        )
        user = User.objects.get(id=self.user1.id)
        serializer = UserSerializer(user, context={'request': self.request})
        response_data = dict(sorted(response.data.items()))
        serializer_data = dict(sorted(serializer.data.items()))
        # print("response data: ", response_data)
        # print("serializer data: ", serializer_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, serializer_data)

    def test_update_user(self):
        data = {
            'email': 'newtester1@email.com',
        }
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(
            reverse('user-detail', args=[self.user1.id]), data, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.user1.refresh_from_db()
        self.assertEqual(
            check_password('IHBD089HJS', self.user1.password, ), True
        )
        self.assertEqual(
            self.user1.email, 'newtester1@email.com'
        )

    def test_delete_user(self):
        self.client.force_authenticate(user=self.user1)
        data = {'current_password': 'IHBD089HJS'}
        response = self.client.delete(
            reverse('user-detail', args=[self.user1.id]), data=data
        )
        # print(response.data)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            User.objects.all().count(), 1
        )

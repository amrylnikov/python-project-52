from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class TaskTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='username',
            first_name='first_name',
            last_name='last_name',
            password='password',
        )
        self.user_new = User.objects.create_user(
            username='username_new',
            first_name='first_name_new',
            last_name='last_name',
            password='password_new',
        )
        self.client.login(username='username', password='password')
        self.status = Status.objects.create(name='status_name')
        self.label = Label.objects.create(name='label_name')
        self.task = Task.objects.create(
            name='Task 1',
            description='Description of Task 1',
            status=self.status,
            author=self.user,
            executor=self.user
        )
        self.task_form_data = {
            'name': 'new name',
            'description': 'new description',
            'status': self.status.id,
            'labels': [self.label.id],
        }
        self.task.labels.add(self.label)

    def test_create_task(self):

        create_url = reverse('create_task')

        response = self.client.post(create_url, self.task_form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('tasks'))
        self.assertEqual(Task.objects.count(), 2)

        new_task = Task.objects.get(pk=2)

        self.assertEqual(new_task.name, 'new name')
        self.assertEqual(new_task.description, 'new description')

    def test_edit_task(self):
        edit_url = reverse('edit_task', args=[1])

        response = self.client.get(edit_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/update.html')

        response = self.client.post(edit_url, self.task_form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('tasks'))

        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'new name')
        self.assertEqual(self.task.description, 'new description')

        create_url = reverse('create_task')
        new_edit_url = reverse('edit_task', args=[2])

        self.client.post(create_url, self.task_form_data)

        login_data = {
            'username': 'username_new',
            'password': 'password_new',
        }

        login_url = reverse('login')
        self.client.post(login_url, login_data)

        response = self.client.post(new_edit_url)

        self.assertEqual(response.status_code, 403)

    def test_delete_task(self):
        delete_url = reverse('delete_task', args=[1])

        response = self.client.get(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/task_confirm_delete.html')

        response = self.client.post(delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('tasks'))

        with self.assertRaises(Task.DoesNotExist):
            self.task.refresh_from_db()

        create_url = reverse('create_task')
        new_delete_url = reverse('delete_task', args=[2])

        self.client.post(create_url, self.task_form_data)

        login_data = {
            'username': 'username_new',
            'password': 'password_new',
        }

        login_url = reverse('login')
        self.client.post(login_url, login_data)

        response = self.client.post(new_delete_url)

        self.assertEqual(response.status_code, 403)

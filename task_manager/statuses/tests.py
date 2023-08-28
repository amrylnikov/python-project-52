from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from task_manager.statuses.models import Status


class StatusesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.form_data = {
            'name': 'old_name',
        }
        self.create_url = reverse('create_status')
        self.edit_url = reverse('edit_status', args=[1])
        self.delete_url = reverse('delete_status', args=[1])
        self.user = User.objects.create_user(
            username='username',
            first_name='first_name',
            last_name='last_name',
            password='password',
        )
        self.client.login(username='username', password='password')
        self.status = Status.objects.create(
            name='name',
        )

    def test_create_status(self):
        response = self.client.post(self.create_url, self.form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('statuses'))
        self.assertEqual(Status.objects.count(), 2)

    def test_edit_status(self):
        response = self.client.get(self.edit_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')

        new_form_data = {
            'name': 'new_name',
        }

        response = self.client.post(self.edit_url, new_form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('statuses'))

        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'new_name')

    def test_delete_status(self):
        response = self.client.get(self.delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/status_confirm_delete.html')

        response = self.client.post(self.delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('statuses'))

        with self.assertRaises(Status.DoesNotExist):
            self.status.refresh_from_db()

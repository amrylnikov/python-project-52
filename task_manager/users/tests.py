from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class UserRegisterTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('registration')
        self.login_url = reverse('login')
        self.form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        self.edit_url = reverse('edit', args=[1])
        self.delete_url = reverse('delete', args=[1])
        self.login_data = {
            'username': self.form_data['username'],
            'password': self.form_data['password1'],
        }

    def test_registration(self):
        response = self.client.post(self.register_url, self.form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)
        self.assertEqual(User.objects.count(), 1)

    def test_login(self):
        self.client.post(self.register_url, self.form_data)

        response = self.client.post(self.login_url, self.login_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_edit_user(self):
        self.client.post(self.register_url, self.form_data)
        self.user = User.objects.get(username='testuser')

        response = self.client.get(self.edit_url)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'user_update.html')

        new_form_data = {
            'username': 'Updated',
            'first_name': 'User',
            'last_name': 'qwerqwer',
            'password1': 'testpassword1',
            'password2': 'testpassword1',
        }

        response = self.client.post(self.edit_url, new_form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users'))

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'Updated')
        self.assertEqual(self.user.first_name, 'User')

    def test_delete_user(self):
        self.client.post(self.register_url, self.form_data)
        self.user = User.objects.get(username='testuser')

        response = self.client.get(self.delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'auth/user_confirm_delete.html')

        response = self.client.post(self.delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users'))

        with self.assertRaises(User.DoesNotExist):
            self.user.refresh_from_db()

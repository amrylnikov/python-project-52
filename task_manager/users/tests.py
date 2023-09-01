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
        self.user = User.objects.create_user(
            username='username',
            first_name='first_name',
            last_name='last_name',
            password='password',
        )
        self.client.login(username='username', password='password')

    def test_registration(self):
        response = self.client.post(self.register_url, self.form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

        new_user = User.objects.get(pk=2)

        self.assertEqual(new_user.username, 'testuser')
        self.assertEqual(new_user.first_name, 'Test')
        self.assertEqual(new_user.last_name, 'User')

    def test_login(self):
        login_data = {
            'username': 'username',
            'password': 'password',
        }

        response = self.client.post(self.login_url, login_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_edit_user(self):
        edit_url = reverse('edit', args=[1])

        response = self.client.get(edit_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_update.html')

        response = self.client.post(edit_url, self.form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users'))

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')

    def test_delete_user(self):
        delete_url = reverse('delete', args=[1])

        response = self.client.get(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/user_confirm_delete.html')

        response = self.client.post(delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users'))

        with self.assertRaises(User.DoesNotExist):
            self.user.refresh_from_db()

    def test_access_user(self):
        self.client.post(self.register_url, self.form_data)

        edit_url = reverse('edit', args=[1])
        login_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }

        self.client.post(self.login_url, login_data)

        response = self.client.post(edit_url)

        self.assertEqual(response.status_code, 403)

        delete_url = reverse('delete', args=[1])

        response = self.client.post(delete_url)

        self.assertEqual(response.status_code, 403)

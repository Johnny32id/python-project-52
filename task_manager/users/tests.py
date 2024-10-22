from django.test import Client
from django.test.testcases import TestCase
from django.urls import reverse

from task_manager.users.models import User


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            username='testuser',
            password='password123'
        )
        self.client = Client()
        self.client.force_login(self.user)


class UserIndexViewTest(TestCase):
    def test_user_index_view_get(self):
        response = self.client.get(reverse('users_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')


class UserCreateViewTest(TestCase):
    def test_user_create_view_get(self):
        response = self.client.get(reverse('users_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create.html')

    def test_user_create_view_post_valid(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'password123'
        }
        self.assertEqual(User.objects.count(), 0)
        response = self.client.post(reverse('users_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(User.objects.count(), 1)

    def test_user_create_view_post_invalid(self):
        data = {
            'first_name': '',
            'last_name': '',
            'username': '',
            'password1': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(reverse('users_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create.html')
        self.assertEqual(User.objects.count(), 0)


class UserUpdateViewTest(BaseTestCase):
    def test_user_update_view_get(self):
        response = self.client.get(reverse('users_update', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update.html')

    def test_user_update_view_post_valid(self):
        data = {
            'first_name': 'New Test',
            'last_name': 'New User',
            'username': 'newtestuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(
            reverse('users_update', args=[self.user.pk]),
            data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_index'))
        self.assertFalse(self.client.session.get('user_id'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'New Test')
        self.assertEqual(self.user.last_name, 'New User')
        self.assertEqual(self.user.username, 'newtestuser')

    def test_user_update_view_post_invalid(self):
        data = {
            'first_name': '',
            'last_name': '',
            'username': '',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(
            reverse('users_update', args=[self.user.pk]),
            data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update.html')
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.username, 'testuser')


class UserDeleteViewTest(BaseTestCase):
    def test_user_delete_view_get(self):
        self.assertEqual(User.objects.count(), 1)
        response = self.client.get(reverse('users_delete', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete.html')

    def test_user_delete_view_post(self):
        response = self.client.post(reverse('users_delete', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_index'))
        self.assertEqual(User.objects.count(), 0)
        self.assertQuerySetEqual(User.objects.filter(pk=self.user.pk), [])


class ChangeOtherUserProfileTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            first_name='Test1',
            last_name='User1',
            username='testuser1',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            first_name='Test2',
            last_name='User2',
            username='testuser2',
            password='password123'
        )

    def test_authorized_user_cannot_change_other_user_profile(self):
        self.client.force_login(self.user1)
        self.assertEqual(User.objects.count(), 2)

        response = self.client.post(
            reverse('users_update', kwargs={'pk': self.user2.pk}),
            data={'username': 'Buzz', 'first_name': 'Bar'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_index'))

        response = self.client.post(
            reverse('users_delete', kwargs={'pk': self.user2.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_index'))

        self.user2.refresh_from_db()
        self.assertEqual(self.user2.username, 'testuser2')
        self.assertEqual(self.user2.first_name, 'Test2')
        self.assertEqual(User.objects.count(), 2)

    def test_not_authorized_user_cannot_change_other_user_profile(self):

        self.assertEqual(User.objects.count(), 2)

        response = self.client.post(
            reverse('users_update', kwargs={'pk': self.user1.pk}),
            data={'username': 'Buzz', 'first_name': 'Bar'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        response = self.client.post(
            reverse('users_delete', kwargs={'pk': self.user1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'testuser1')
        self.assertEqual(self.user1.first_name, 'Test1')
        self.assertEqual(User.objects.count(), 2)


class UserLoginTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_user_login(self):
        response = self.client.post(
            reverse('login'),
            data={'username': 'testuser', 'password': 'password123'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))


class UserLogoutTest(BaseTestCase):
    def test_user_logout(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

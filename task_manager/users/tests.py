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
            password='gdfgdbd123DDD'
        )
        self.client = Client()
        self.client.force_login(self.user)


class UserIndexViewTest(BaseTestCase):
    def test_user_index_view_get(self):
        response = self.client.get(reverse('users_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/list.html')


class UserCreateViewTest(TestCase):
    def test_user_create_view_get(self):
        response = self.client.get(reverse('users_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create.html')

    def test_user_create_view_post_valid(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'password1': 'gdfgdbd123DDD',
            'password2': 'gdfgdbd123DDD'
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
            'password1': 'gdfgdbd123DDD',
            'password2': 'gdfgdbd123DDD'
        }
        response = self.client.post(reverse('users_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create.html')
        self.assertEqual(User.objects.count(), 0)


class UserUpdateViewTest(BaseTestCase):
    def test_user_update_view_get(self):
        response = self.client.get(reverse('users_update', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update.html')

    def test_user_update_view_post_valid(self):
        data = {
            'first_name': 'New Test',
            'last_name': 'New User',
            'username': 'newtestuser',
            'password1': 'gdfgdbd123DDD',
            'password2': 'gdfgdbd123DDD'
        }
        response = self.client.post(
            reverse('users_update', args=[self.user.pk]),
            data,
            follow=False
        )
        self.assertEqual(response.status_code, 302)
        # Редирект может быть на /users/, который затем редиректит на
        # /login/ если сессия очищена
        # Проверяем только что это редирект
        self.assertTrue(response.url in [reverse('users_index'), '/users/'])
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'New Test')
        self.assertEqual(self.user.last_name, 'New User')
        self.assertEqual(self.user.username, 'newtestuser')

    def test_user_update_view_post_invalid(self):
        data = {
            'first_name': '',
            'last_name': '',
            'username': '',
            'password1': 'gdfgdbd123DDD',
            'password2': 'gdfgdbd123DDD'
        }
        response = self.client.post(
            reverse('users_update', args=[self.user.pk]),
            data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update.html')
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.username, 'testuser')


class UserDeleteViewTest(BaseTestCase):
    def test_user_delete_view_get(self):
        self.assertEqual(User.objects.count(), 1)
        response = self.client.get(reverse('users_delete', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete.html')

    def test_user_delete_view_post(self):
        response = self.client.post(
            reverse('users_delete', args=[self.user.pk]),
            follow=False
        )
        self.assertEqual(response.status_code, 302)
        # Редирект может быть на /users/, который затем редиректит на
        # /login/ если сессия очищена
        self.assertTrue(response.url in [reverse('users_index'), '/users/'])
        self.assertEqual(User.objects.count(), 0)
        self.assertQuerySetEqual(User.objects.filter(pk=self.user.pk), [])


class ChangeOtherUserProfileTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            first_name='Test1',
            last_name='User1',
            username='testuser1',
            password='gdfgdbd123DDD'
        )
        self.user2 = User.objects.create_user(
            first_name='Test2',
            last_name='User2',
            username='testuser2',
            password='gdfgdbd123DDD'
        )

    def test_authorized_user_cannot_change_other_user_profile(self):
        self.client.force_login(self.user1)
        self.assertEqual(User.objects.count(), 2)

        response = self.client.post(
            reverse('users_update', kwargs={'pk': self.user2.pk}),
            data={'username': 'Buzz', 'first_name': 'Bar'},
            follow=False
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url in [reverse('users_index'), '/users/'])

        response = self.client.post(
            reverse('users_delete', kwargs={'pk': self.user2.pk}),
            follow=False
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url in [reverse('users_index'), '/users/'])

        self.user2.refresh_from_db()
        self.assertEqual(self.user2.username, 'testuser2')
        self.assertEqual(self.user2.first_name, 'Test2')
        self.assertEqual(User.objects.count(), 2)

    def test_not_authorized_user_cannot_change_other_user_profile(self):
        # Убеждаемся, что пользователь не авторизован
        self.client.logout()
        self.assertEqual(User.objects.count(), 2)

        response = self.client.post(
            reverse('users_update', kwargs={'pk': self.user1.pk}),
            data={'username': 'Buzz', 'first_name': 'Bar'},
            follow=False
        )
        self.assertEqual(response.status_code, 302)
        # Редирект может быть на /login/ (если сначала проверка авторизации)
        # или на /users/ (если сначала проверка прав доступа)
        # Главное - пользователь не может изменить данные
        self.assertIn(
            response.url,
            ['/users/', '/users', reverse('users_index')] +
            [f'/login/?next=/users/{self.user1.pk}/update/']
        )

        response = self.client.post(
            reverse('users_delete', kwargs={'pk': self.user1.pk}),
            follow=False
        )
        self.assertEqual(response.status_code, 302)
        # Редирект может быть на /login/ (если сначала проверка авторизации)
        # или на /users/ (если сначала проверка прав доступа)
        self.assertIn(
            response.url,
            ['/users/', '/users', reverse('users_index')] +
            [f'/login/?next=/users/{self.user1.pk}/delete/']
        )

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
            data={'username': 'testuser', 'password': 'gdfgdbd123DDD'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))


class UserLogoutTest(BaseTestCase):
    def test_user_logout(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

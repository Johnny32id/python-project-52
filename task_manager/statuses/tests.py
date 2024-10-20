from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status

User = get_user_model()


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


class UnauthorizedCRUDTest(TestCase):
    def test_unauthorized_index_view(self):
        response = self.client.get(reverse('statuses_index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_unauthorized_create(self):
        response = self.client.get(reverse('statuses_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_unauthorized_update(self):
        response = self.client.get(reverse('statuses_update', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_unauthorized_delete(self):
        response = self.client.get(reverse('statuses_delete', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))


class StatusesIndexViewTest(BaseTestCase):
    def test_statuses_index_view(self):
        response = self.client.get(reverse('statuses_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/index.html')


class StatusesCreateViewTest(BaseTestCase):
    def test_status_create_view_get(self):
        response = self.client.get(reverse('statuses_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')

    def test_status_create_view_post_valid(self):
        data = {
            'name': 'Test status'
        }
        self.assertEqual(Status.objects.count(), 0)
        response = self.client.post(reverse('statuses_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertEqual(Status.objects.count(), 1)
        status = Status.objects.first()
        self.assertEqual(status.name, 'Test status')

    def test_status_create_view_post_invalid(self):
        data = {
            'name': ''
        }
        response = self.client.post(reverse('statuses_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')
        self.assertContains(response, _('This field is required.'))
        self.assertEqual(Status.objects.count(), 0)

    def test_status_create_view_post_unique(self):
        data = {
            'name': 'Test status'
        }
        self.assertEqual(Status.objects.count(), 0)
        self.client.post(reverse('statuses_create'), data)
        response = self.client.post(reverse('statuses_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')
        self.assertEqual(Status.objects.count(), 1)


class StatusesUpdateViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.status = Status.objects.create(name='Test status')

    def test_status_update_view_get(self):
        response = self.client.get(
            reverse('statuses_update', kwargs={'pk': self.status.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')

    def test_status_update_view_post_valid(self):
        data = {
            'name': 'Test status updated'
        }
        self.assertEqual(Status.objects.count(), 1)
        response = self.client.post(
            reverse('statuses_update', kwargs={'pk': self.status.pk}), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertEqual(Status.objects.count(), 1)
        status = Status.objects.first()
        self.assertEqual(status.name, 'Test status updated')

    def test_status_update_view_post_invalid(self):
        data = {
            'name': ''
        }
        self.assertEqual(Status.objects.count(), 1)
        response = self.client.post(
            reverse('statuses_update', kwargs={'pk': self.status.pk}), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')
        self.assertContains(response, _('This field is required.'))
        self.assertEqual(Status.objects.count(), 1)
        status = Status.objects.first()
        self.assertEqual(status.name, 'Test status')

    def test_status_update_view_post_unique(self):
        data_new = {
            'name': 'Test status new'
        }
        self.assertEqual(Status.objects.count(), 1)
        response = self.client.post(reverse('statuses_create'), data_new)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertEqual(Status.objects.count(), 2)

        status1 = Status.objects.first()
        data = {
            'name': 'Test status new'
        }
        response = self.client.post(
            reverse('statuses_update', kwargs={'pk': status1.pk}), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')
        self.assertEqual(Status.objects.count(), 2)
        self.assertEqual(Status.objects.first().name, 'Test status')


class StatusesDeleteViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.status = Status.objects.create(name='Test status')

    def test_status_delete_view(self):
        response = self.client.get(
            reverse('statuses_delete', kwargs={'pk': self.status.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/delete.html')

    def test_status_delete_view_post(self):
        self.assertEqual(Status.objects.count(), 1)
        response = self.client.post(
            reverse('statuses_delete', kwargs={'pk': self.status.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertEqual(Status.objects.count(), 0)

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label

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
        response = self.client.get(reverse('labels_index'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_unauthorized_create(self):
        response = self.client.get(reverse('labels_create'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_unauthorized_update(self):
        response = self.client.get(reverse('labels_update', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_unauthorized_delete(self):
        response = self.client.get(reverse('labels_delete', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))


class LabelsIndexViewTest(BaseTestCase):
    def test_labels_index_view(self):
        response = self.client.get(reverse('labels_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/list.html')


class LabelsCreateViewTest(BaseTestCase):
    def test_label_create_view_get(self):
        response = self.client.get(reverse('labels_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create.html')

    def test_label_create_view_post_valid(self):
        data = {
            'name': 'Test label'
        }
        self.assertEqual(Label.objects.count(), 0)
        response = self.client.post(reverse('labels_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Label.objects.count(), 1)
        label = Label.objects.first()
        self.assertEqual(label.name, 'Test label')

    def test_label_create_view_post_invalid(self):
        data = {
            'name': ''
        }
        response = self.client.post(reverse('labels_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create.html')
        self.assertContains(response, _('This field is required.'))
        self.assertEqual(Label.objects.count(), 0)

    def test_label_create_view_post_unique(self):
        data = {
            'name': 'Test label'
        }
        self.assertEqual(Label.objects.count(), 0)
        self.client.post(reverse('labels_create'), data)
        response = self.client.post(reverse('labels_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create.html')
        self.assertEqual(Label.objects.count(), 1)


class LabelsUpdateViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.label = Label.objects.create(name='Test label')

    def test_label_update_view_get(self):
        response = self.client.get(
            reverse('labels_update', kwargs={'pk': self.label.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update.html')

    def test_label_update_view_post_valid(self):
        data = {
            'name': 'Test label updated'
        }
        self.assertEqual(Label.objects.count(), 1)
        response = self.client.post(
            reverse('labels_update', kwargs={'pk': self.label.pk}), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Label.objects.count(), 1)
        label = Label.objects.first()
        self.assertEqual(label.name, 'Test label updated')

    def test_label_update_view_post_invalid(self):
        data = {
            'name': ''
        }
        self.assertEqual(Label.objects.count(), 1)
        response = self.client.post(
            reverse('labels_update', kwargs={'pk': self.label.pk}), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update.html')
        self.assertEqual(Label.objects.count(), 1)
        label = Label.objects.first()
        self.assertEqual(label.name, 'Test label')

    def test_label_update_view_post_unique(self):
        data_new = {
            'name': 'Test label new'
        }
        self.assertEqual(Label.objects.count(), 1)
        response = self.client.post(reverse('labels_create'), data_new)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Label.objects.count(), 2)

        label1 = Label.objects.first()
        data = {
            'name': 'Test label new'
        }
        response = self.client.post(
            reverse('labels_update', kwargs={'pk': label1.pk}), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update.html')
        self.assertEqual(Label.objects.count(), 2)
        self.assertEqual(Label.objects.first().name, 'Test label')


class LabelsDeleteViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.label = Label.objects.create(name='Test label')

    def test_label_delete_view(self):
        response = self.client.get(
            reverse('labels_delete', kwargs={'pk': self.label.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete.html')

    def test_label_delete_view_post(self):
        self.assertEqual(Label.objects.count(), 1)
        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': self.label.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Label.objects.count(), 0)

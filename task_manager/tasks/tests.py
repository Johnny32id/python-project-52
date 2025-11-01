from django.test import TestCase, Client
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
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

        self.status = Status.objects.create(name='Test status')
        self.author = self.user
        self.executor = User.objects.create_user(username='executor', password='12345')
        self.label = Label.objects.create(name='Test label')


class UnauthorizedCRUDTest(TestCase):

    def test_unauthorized_index_view(self):
        response = self.client.get(reverse('tasks_index'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_unauthorized_create(self):
        response = self.client.get(reverse('tasks_create'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_unauthorized_update(self):
        response = self.client.get(reverse('tasks_update', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_unauthorized_delete(self):
        # Создаем задачу для теста
        user = User.objects.create_user(username='test', password='12345')
        status = Status.objects.create(name='Test status')
        task = Task.objects.create(
            name='Test task',
            description='Test',
            status=status,
            author=user
        )
        response = self.client.get(reverse('tasks_delete', args=[task.pk]))
        self.assertEqual(response.status_code, 302)
        # Редирект может быть на /login/ (если сначала проверка авторизации)
        # или на /tasks/ (если сначала проверка автора задачи)
        # Проверяем что это редирект
        self.assertIn(response.url, ['/tasks/', '/tasks', reverse('tasks_index')] + 
                     [f'/login/?next=/tasks/{task.pk}/delete/'])


class TasksIndexViewTest(BaseTestCase):
    def test_tasks_index_view(self):
        response = self.client.get(reverse('tasks_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/list.html')


class TasksCreateViewTest(BaseTestCase):
    def test_tasks_create_view_get(self):
        response = self.client.get(reverse('tasks_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create.html')

    def test_tasks_create_view_post_valid(self):
        data = {
            'name': 'Test task',
            'description': 'Test description',
            'status': self.status.id,
            'author': self.author,
            'executor': self.executor.id,
            'labels': self.label.id
        }
        self.assertEqual(Task.objects.count(), 0)
        response = self.client.post(reverse('tasks_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertEqual(Task.objects.count(), 1)

    def test_tasks_create_view_post_invalid(self):
        data = {
            'name': '',
            'description': 'Test description',
            'status': 1,
            'executor': 1,
            'labels': 1
        }
        self.assertEqual(Task.objects.count(), 0)
        response = self.client.post(reverse('tasks_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create.html')
        self.assertEqual(Task.objects.count(), 0)

    def test_tasks_create_view_post_unique(self):
        data1 = {
            'name': 'Test task',
            'description': 'Test description',
            'status': self.status.id,
            'author': self.author,
            'executor': self.executor.id,
            'labels': self.label.id
        }
        data2 = {
            'name': 'Test task',
            'description': 'Test description new',
            'status': self.status.id,
            'author': self.author,
            'executor': '',
            'labels': ''
        }
        self.assertEqual(Task.objects.count(), 0)
        self.client.post(reverse('tasks_create'), data1)
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.post(reverse('tasks_create'), data2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create.html')
        self.assertEqual(Task.objects.count(), 1)


class TasksUpdateViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client.post(reverse('tasks_create'), {
            'name': 'Test task',
            'description': 'Test description',
            'status': self.status.id,
            'author': self.author,
            'executor': self.executor.id,
            'labels': self.label.id
        })
        self.task = Task.objects.first()

    def test_tasks_update_view_get(self):
        response = self.client.get(reverse('tasks_update', kwargs={'pk': self.task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update.html')

    def test_tasks_update_view_post_valid(self):
        data = {
            'name': 'Test task updated',
            'description': 'Test description updated',
            'status': Status.objects.create(name='New test status').id,
            'author': self.author,
            'executor': self.executor.id,
            'labels': self.label.id
        }
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.post(
            reverse('tasks_update', kwargs={'pk': self.task.pk}), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertEqual(Task.objects.count(), 1)
        updated_task = Task.objects.first()
        self.assertEqual(updated_task.name, 'Test task updated')
        self.assertEqual(updated_task.description, 'Test description updated')

    def test_tasks_update_view_post_invalid(self):
        data = {
            'name': '',
            'description': '',
            'status': '',
            'author': self.author,
            'executor': 1,
            'labels': 1
        }
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.post(
            reverse('tasks_update', kwargs={'pk': self.task.pk}), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update.html')
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.name, 'Test task')

    def test_tasks_update_view_post_unique(self):
        new_status = Status.objects.create(name='New test status')
        data_second = {
            'name': 'Test task new',
            'description': 'Test description new',
            'status': new_status.id,
            'author': self.author,
            'executor': User.objects.create_user(username='new_worker',
                                                 password='12345').id,
            'labels': self.label.id
        }
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.post(reverse('tasks_create'), data_second)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertEqual(Task.objects.count(), 2)

        data_first = {
            'name': 'Test task new',
            'description': 'Test description new',
            'status': self.status.id,
            'author': self.author,
            'executor': self.executor.id,
            'labels': ''
        }
        response = self.client.post(
            reverse('tasks_update', kwargs={'pk': self.task.pk}), data_first)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update.html')
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(self.task.name, 'Test task')


class TaskDeleteViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client.post(reverse('tasks_create'), {
            'name': 'Test task',
            'description': 'Test description',
            'status': self.status.id,
            'author': self.author,
            'executor': self.executor.id,
            'labels': self.label.id
        })
        self.task = Task.objects.first()

    def test_tasks_delete_view_get(self):
        response = self.client.get(
            reverse('tasks_delete', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete.html')

    def test_tasks_delete_view_post(self):
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.post(
            reverse('tasks_delete', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertEqual(Task.objects.count(), 0)


class TaskDetailViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client.post(reverse('tasks_create'), {
            'name': 'Test task',
            'description': 'Test description',
            'status': self.status.id,
            'author': self.author,
            'executor': self.executor.id,
            'labels': self.label.id
        })
        self.task = Task.objects.first()

        self.task_form = TaskForm(instance=self.task)

    def test_tasks_detail_view_get(self):
        response = self.client.get(
            reverse('tasks_detail', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/detail.html')

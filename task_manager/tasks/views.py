from typing import Any, Dict, Type

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_filters.views import FilterView

from task_manager.base_views import (BaseListView,
                                     BaseCreateView,
                                     BaseUpdateView,
                                     BaseDetailView,
                                     BaseDeleteView)
from task_manager.tasks.filters import TaskFilterForm
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TaskListView(FilterView, BaseListView):
    """Представление для отображения списка задач с фильтрацией."""

    template_name = 'tasks/list.html'
    model = Task
    filterset_class = TaskFilterForm
    context_object_name = 'tasks'

    def get_filterset_kwargs(
        self, filterset_class: Type[TaskFilterForm]
    ) -> Dict[str, Any]:
        """
        Передает request в FilterSet для доступа к пользователю.

        Args:
            filterset_class: Класс фильтра для задач.

        Returns:
            Dict[str, Any]: Словарь аргументов для инициализации FilterSet.
        """
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['request'] = self.request
        return kwargs


class TaskCreateView(BaseCreateView):
    """Представление для создания новой задачи."""

    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks_index')
    success_message = _('Task successfully created')
    create_title = _('Create task')
    action_url = 'tasks_create'
    button_label = _('Create')

    def form_valid(self, form: TaskForm) -> HttpResponse:
        """
        Обрабатывает валидную форму задачи.

        Устанавливает автора задачи на текущего пользователя.

        Args:
            form: Валидная форма задачи.

        Returns:
            HttpResponse: Ответ после успешной обработки формы.
        """
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return response


class TaskDetailView(BaseDetailView):
    """Представление для детального просмотра задачи."""

    template_name = 'tasks/detail.html'
    model = Task
    pk_url_kwarg = 'pk'
    context_object_name = 'task'
    form_class = TaskForm


class TaskUpdateView(BaseUpdateView):
    """Представление для обновления задачи."""

    form_class = TaskForm
    model = Task
    success_url = reverse_lazy('tasks_index')
    success_message = _('Task successfully updated')
    update_title = _('Change task')
    action_url = 'tasks_update'
    button_label = _('Change')


class TaskDeleteView(BaseDeleteView):
    """Представление для удаления задачи."""

    model = Task
    success_url = reverse_lazy('tasks_index')
    success_message = _('Task successfully deleted')
    delete_title = _('Deleting a task')

    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """
        Проверяет права доступа перед удалением задачи.

        Только автор задачи может её удалить.

        Args:
            request: HTTP запрос от клиента.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            HttpResponse: Редирект на список задач, если нет прав,
                или результат родительского метода.
        """
        task = self.get_object()
        if task.author != request.user:
            messages.error(request, _('Only the author can delete the task'))
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

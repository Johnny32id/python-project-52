from typing import Any

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.base_views import (BaseListView,
                                     BaseCreateView,
                                     BaseUpdateView,
                                     BaseDeleteView)
from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class LabelListView(BaseListView):
    """Представление для отображения списка меток."""

    template_name = 'labels/list.html'
    model = Label
    context_object_name = 'labels'


class LabelCreateView(BaseCreateView):
    """Представление для создания новой метки."""

    form_class = LabelForm
    model = Label
    success_url = reverse_lazy('labels_index')
    success_message = _('Label successfully created')
    create_title = _('Create label')
    action_url = 'labels_create'
    button_label = _('Create')


class LabelUpdateView(BaseUpdateView):
    """Представление для обновления метки."""

    form_class = LabelForm
    model = Label
    success_url = reverse_lazy('labels_index')
    success_message = _('Label successfully updated')
    update_title = _('Change label')
    action_url = 'labels_update'
    button_label = _('Update')


class LabelDeleteView(BaseDeleteView):
    """Представление для удаления метки."""

    model = Label
    success_url = reverse_lazy('labels_index')
    success_message = _('Label successfully deleted')
    protected_error_message = _('Cannot delete label because it is in use')
    delete_title = _('Deleting a label')

    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """
        Обрабатывает запрос POST на удаление метки.

        Проверяет, используется ли метка в задачах, и если да,
        показывает сообщение об ошибке вместо удаления.

        Args:
            request: HTTP запрос от клиента.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            HttpResponse: Ответ от родительского метода или редирект
                при использовании метки в задачах.
        """
        label = self.get_object()
        # Проверяем, используется ли метка в задачах
        if Task.objects.filter(labels=label).exists():
            messages.error(request, self.protected_error_message)
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)

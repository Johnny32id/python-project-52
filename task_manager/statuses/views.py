from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.base_views import (BaseListView,
                                     BaseCreateView,
                                     BaseUpdateView,
                                     BaseDeleteView)
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class StatusListView(BaseListView):
    """Представление для отображения списка статусов."""

    template_name = 'statuses/list.html'
    model = Status
    context_object_name = 'statuses'


class StatusCreateView(BaseCreateView):
    """Представление для создания нового статуса."""

    form_class = StatusForm
    model = Status
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status successfully created')
    create_title = _('Create status')
    action_url = 'statuses_create'
    button_label = _('Create')


class StatusUpdateView(BaseUpdateView):
    """Представление для обновления статуса."""

    form_class = StatusForm
    model = Status
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status successfully updated')
    update_title = _('Change status')
    action_url = 'statuses_update'
    button_label = _('Change')


class StatusDeleteView(BaseDeleteView):
    """Представление для удаления статуса."""

    model = Status
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status successfully deleted')
    protected_error_message = _('Cannot delete status because it is in use')
    delete_title = _('Deleting a status')

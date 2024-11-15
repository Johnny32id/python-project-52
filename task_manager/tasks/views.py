from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_filters.views import FilterView

from task_manager.views import (BaseListView,
                                BaseCreateView,
                                BaseUpdateView,
                                BaseDetailView,
                                BaseDeleteView)
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.filters import TaskFilterForm
from task_manager.tasks.models import Task


class TaskListView(FilterView, BaseListView):
    template_name = 'tasks/index.html'
    model = Task
    filterset_class = TaskFilterForm
    context_object_name = 'tasks'


class TaskCreateView(BaseCreateView):
    template_name = 'tasks/create.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks_index')
    success_message = _('Task successfully created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return response


class TaskDetailView(BaseDetailView):
    template_name = 'tasks/detail.html'
    model = Task
    pk_url_kwarg = 'pk'
    context_object_name = 'task'
    form_class = TaskForm


class TaskUpdateView(BaseUpdateView):
    template_name = 'tasks/update.html'
    form_class = TaskForm
    model = Task
    success_url = reverse_lazy('tasks_index')
    success_message = _('Task successfully updated')


class TaskDeleteView(BaseDeleteView):
    template_name = 'tasks/delete.html'
    model = Task
    success_url = reverse_lazy('tasks_index')
    success_message = _('Task successfully deleted')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if response.status_code != 302:
            task = self.get_object()
            if task.author != request.user:
                messages.error(request,
                               _('Only the author can delete the task'))
                return redirect(self.success_url)
        return response

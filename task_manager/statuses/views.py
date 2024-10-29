from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.views import (BaseIndexView,
                                BaseCreateView,
                                BaseUpdateView,
                                BaseDeleteView)
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class IndexView(BaseIndexView):
    template_name = 'statuses/index.html'
    model = Status
    context_object_name = 'statuses'


class StatusCreateView(BaseCreateView):
    template_name = 'statuses/create.html'
    form_class = StatusForm
    model = Status
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status successfully created')


class StatusUpdateView(BaseUpdateView):
    template_name = 'statuses/update.html'
    form_class = StatusForm
    model = Status
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status successfully updated')


class StatusDeleteView(BaseDeleteView):
    template_name = 'statuses/delete.html'
    model = Status
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status successfully deleted')
    error_message = _('Cannot delete status because it is in use')

    def post(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            if response.status_code == 302:
                messages.success(request, self.success_message)
            return response
        except ProtectedError:
            messages.error(request, self.error_message)
            return redirect(self.success_url)

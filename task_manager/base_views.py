from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import BaseLoginRequiredMixin, ProtectedErrorHandlerMixin
from django.views.generic import (ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  DetailView)


class BaseListView(BaseLoginRequiredMixin,
                   ListView):
    pass


class BaseCreateView(BaseLoginRequiredMixin,
                     SuccessMessageMixin,
                     CreateView):
    pass


class BaseUpdateView(BaseLoginRequiredMixin,
                     SuccessMessageMixin,
                     UpdateView):
    pass


class BaseDeleteView(ProtectedErrorHandlerMixin,
                     BaseLoginRequiredMixin,
                     SuccessMessageMixin,
                     DeleteView):
    pass


class BaseDetailView(BaseLoginRequiredMixin,
                     SuccessMessageMixin,
                     DetailView):
    pass

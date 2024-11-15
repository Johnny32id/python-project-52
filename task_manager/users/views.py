from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.mixins import AuthAndProfileOwnershipMixin, ProtectedErrorHandlerMixin
from task_manager.users.forms import UserForm
from task_manager.users.models import User


class UserListView(ListView):
    template_name = 'users/index.html'
    model = User
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'users/create.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered')


class UserUpdateView(AuthAndProfileOwnershipMixin,
                     SuccessMessageMixin,
                     UpdateView):
    template_name = 'users/update.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users_index')
    success_message = _('User successfully updated')


class UserDeleteView(AuthAndProfileOwnershipMixin,
                     SuccessMessageMixin,
                     ProtectedErrorHandlerMixin,
                     DeleteView):
    template_name = 'users/delete.html'
    model = User
    success_url = reverse_lazy('users_index')
    success_message = _('User successfully deleted')
    protected_error_message = _('Cannot delete user because it is in use')

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

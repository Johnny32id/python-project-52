from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.views import (BaseListView,
                                BaseCreateView,
                                BaseUpdateView,
                                BaseDeleteView)

from task_manager.mixins import AuthAndProfileOwnershipMixin
from task_manager.users.forms import UserForm
from task_manager.users.models import User


class IndexView(BaseListView):
    template_name = 'users/index.html'
    model = User
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, BaseCreateView):
    template_name = 'users/create.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered')


class UserUpdateView(AuthAndProfileOwnershipMixin,
                     SuccessMessageMixin,
                     BaseUpdateView):
    template_name = 'users/update.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users_index')
    success_message = _('User successfully updated')


class UserDeleteView(AuthAndProfileOwnershipMixin,
                     SuccessMessageMixin,
                     BaseDeleteView):
    template_name = 'users/delete.html'
    model = User
    success_url = reverse_lazy('users_index')
    success_message = _('User successfully deleted')

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _('Cannot delete user because it is in use'))
            return redirect(reverse_lazy('users_index'))

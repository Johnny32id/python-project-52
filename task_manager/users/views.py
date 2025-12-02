from typing import Any, Dict

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView

from task_manager.base_views import BaseUpdateView, BaseDeleteView
from task_manager.mixins import AuthAndProfileOwnershipMixin
from task_manager.users.forms import UserForm
from task_manager.users.models import User


class UserListView(ListView):
    """Представление для отображения списка пользователей."""

    template_name = 'users/list.html'
    model = User
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    """Представление для регистрации нового пользователя."""

    template_name = 'create.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Добавляет контекст для универсального шаблона создания.

        Args:
            **kwargs: Дополнительные аргументы контекста.

        Returns:
            Dict[str, Any]: Словарь контекста с данными для шаблона регистрации.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = _('Registration')
        context['action_url'] = 'users_create'
        context['button_label'] = _('Register')
        return context


class UserUpdateView(AuthAndProfileOwnershipMixin, BaseUpdateView):
    """Представление для обновления профиля пользователя."""

    model = User
    form_class = UserForm
    success_url = reverse_lazy('users_index')
    success_message = _('User successfully updated')
    update_title = _('Change user')
    action_url = 'users_update'
    button_label = _('Change')


class UserDeleteView(AuthAndProfileOwnershipMixin, BaseDeleteView):
    """Представление для удаления пользователя."""

    model = User
    success_url = reverse_lazy('users_index')
    success_message = _('User successfully deleted')
    protected_error_message = _('Cannot delete user because it is in use')
    delete_title = _('Deleting a user')

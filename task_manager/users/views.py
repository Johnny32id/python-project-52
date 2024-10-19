from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from task_manager.mixins import AuthAndProfileOwnershipMixin, \
    SuccessMessageFormContextMixin
from task_manager.users.forms import UserForm


class IndexView(TemplateView):
    template_name = 'users/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = get_user_model().objects.all()
        return context


class UserCreateView(SuccessMessageFormContextMixin, CreateView):
    template_name = 'users/create.html'
    form_class = UserForm
    success_url = reverse_lazy('login')
    success_message = _('Пользователь успешно зарегестрирован')
    model = get_user_model()
    title = _('Регистрация')
    action = _('Зарегистрировать')


class UserUpdateView(AuthAndProfileOwnershipMixin,
                     SuccessMessageFormContextMixin,
                     UpdateView):
    model = get_user_model()
    template_name = 'users/update.html'
    form_class = UserForm
    success_url = reverse_lazy('users_index')
    success_message = _('Пользователь успешно изменён')
    title = _('Изменить пользователя')
    action = _('Изменить')


class UserDeleteView(AuthAndProfileOwnershipMixin,
                     SuccessMessageFormContextMixin,
                     DeleteView):
    model = get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_index')
    success_message = _('Пользователь успешно удалён')

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request,
                           _('Невозможно удалить пользователя, потому что он используется'))
            return redirect(reverse_lazy('users_index'))

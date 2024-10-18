from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, TemplateView, CreateView, UpdateView, \
    DeleteView, DetailView

LOGIN_URL = reverse_lazy('login')


class AuthAndProfileOwnershipMixin(UserPassesTestMixin):

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, _("Вы не авторизированы. Пожалуйста, выполните вход."))
            return redirect('login')
        messages.error(self.request,
                       _("У вас нет прав изменять других пользователей."))
        return redirect('users_index')

    def test_func(self):
        user_id = self.kwargs.get('pk')
        return self.request.user.pk == user_id


class SuccessMessageFormContextMixin(SuccessMessageMixin, FormView):
    title = ''
    action = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['action'] = self.action
        return context


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        return redirect(self.login_url)


class CustomIndexView(CustomLoginRequiredMixin, TemplateView):
    login_url = LOGIN_URL


class CustomCreateView(CustomLoginRequiredMixin, SuccessMessageFormContextMixin,
                       CreateView):
    action = _('Create')
    login_url = LOGIN_URL


class CustomUpdateView(CustomLoginRequiredMixin, SuccessMessageFormContextMixin,
                       UpdateView):
    action = _('Change')
    login_url = LOGIN_URL

    def get_redirect_url(self):
        return self.login_url


class CustomDeleteView(CustomLoginRequiredMixin, SuccessMessageFormContextMixin,
                       DeleteView):
    login_url = LOGIN_URL


class CustomDetailView(CustomLoginRequiredMixin, SuccessMessageFormContextMixin,
                       DetailView):
    login_url = LOGIN_URL
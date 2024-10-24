from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import (ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  DetailView)


class AuthAndProfileOwnershipMixin(UserPassesTestMixin, LoginRequiredMixin):

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, _("You are not authorized! Please log in."))
            return redirect('login')
        messages.error(self.request,
                       _("You don't have permission to change other user"))
        return redirect('users_index')

    def test_func(self):
        user_id = self.kwargs.get('pk')
        return self.request.user.pk == user_id


class ProtectedErrorHandlerMixin:
    protected_error_message = None
    redirect_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)  # noqa
        except ProtectedError:
            messages.error(request, self.protected_error_message)
            return redirect(self.redirect_url)


class CustomIndexView(LoginRequiredMixin,
                      ListView):
    pass


class CustomCreateView(LoginRequiredMixin,
                       SuccessMessageMixin,
                       CreateView):
    pass


class CustomUpdateView(LoginRequiredMixin,
                       SuccessMessageMixin,
                       UpdateView):
    def get_redirect_url(self):
        return self.login_url


class CustomDeleteView(LoginRequiredMixin,
                       SuccessMessageMixin,
                       DeleteView):
    pass


class CustomDetailView(ProtectedErrorHandlerMixin,
                       LoginRequiredMixin,
                       SuccessMessageMixin,
                       DetailView):
    pass

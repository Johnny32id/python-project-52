from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


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


class BaseLoginRequiredMixin(LoginRequiredMixin):
    login_url = LOGIN_URL

    def handle_no_permission(self):
        return redirect(self.login_url)

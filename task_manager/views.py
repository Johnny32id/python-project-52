from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import BaseLoginRequiredMixin, ProtectedErrorHandlerMixin
from django.views.generic import (ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  DetailView)


def index(request):
    return render(request, 'index.html')


class LoginUserView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    success_message = _('You are logged in')


class LogoutUserView(LogoutView):

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, _('You are logged out'))
        return redirect('index')


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


class BaseDeleteView(BaseLoginRequiredMixin,
                     SuccessMessageMixin,
                     DeleteView):
    pass


class BaseDetailView(ProtectedErrorHandlerMixin,
                     BaseLoginRequiredMixin,
                     SuccessMessageMixin,
                     DetailView):
    pass


def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    return render(request, 'errors/500.html', status=500)

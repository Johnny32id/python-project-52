from typing import TYPE_CHECKING

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    pass


def index(request: HttpRequest) -> HttpResponse:
    """
    Главная страница приложения.

    Отображает начальную страницу Task Manager.

    Args:
        request: HTTP запрос от клиента.

    Returns:
        HttpResponse: Ответ с отрендеренным шаблоном index.html.
    """
    return render(request, 'index.html')


class LoginUserView(SuccessMessageMixin, LoginView):
    """Представление для входа пользователя в систему."""

    template_name = 'login.html'
    success_message = _('You are logged in')


class LogoutUserView(LogoutView):
    """Представление для выхода пользователя из системы."""

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Обрабатывает POST запрос для выхода пользователя.

        Выполняет выход пользователя и перенаправляет на главную страницу.

        Args:
            request: HTTP запрос от клиента.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            HttpResponse: Редирект на главную страницу.
        """
        logout(request)
        messages.info(request, _('You are logged out'))
        return redirect('index')


def handler404(request: HttpRequest, exception: Exception) -> HttpResponse:
    """
    Обработчик ошибки 404 (страница не найдена).

    Args:
        request: HTTP запрос от клиента.
        exception: Исключение, вызвавшее ошибку 404.

    Returns:
        HttpResponse: Ответ с шаблоном ошибки 404 и статусом 404.
    """
    return render(request, 'errors/404.html', status=404)


def handler500(request: HttpRequest) -> HttpResponse:
    """
    Обработчик ошибки 500 (внутренняя ошибка сервера).

    Args:
        request: HTTP запрос от клиента.

    Returns:
        HttpResponse: Ответ с шаблоном ошибки 500 и статусом 500.
    """
    return render(request, 'errors/500.html', status=500)

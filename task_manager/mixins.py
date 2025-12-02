from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import ProtectedError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class AuthAndProfileOwnershipMixin(UserPassesTestMixin):
    """Миксин для проверки прав доступа к профилю пользователя."""

    def handle_no_permission(self) -> HttpResponse:
        """
        Обрабатывает случай отсутствия прав доступа.

        Показывает сообщение об ошибке и перенаправляет на список пользователей.

        Returns:
            HttpResponse: Редирект на страницу списка пользователей.
        """
        messages.error(self.request,
                       _("You don't have permission to change other user"))
        return redirect('users_index')

    def test_func(self) -> bool:
        """
        Проверяет, что текущий пользователь является владельцем профиля.

        Returns:
            bool: True, если текущий пользователь является владельцем профиля,
                иначе False.
        """
        user_id = self.kwargs.get('pk')
        if user_id is None:
            return False
        return self.request.user.pk == user_id


class ProtectedErrorHandlerMixin:
    """
    Миксин для обработки ошибок ProtectedError при удалении объектов.

    Требует обязательного определения success_url в дочерних классах.
    """

    protected_error_message = _(
        'Cannot delete this object because it is in use'
    )

    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """
        Обрабатывает запрос POST с обработкой ProtectedError.

        При возникновении ProtectedError показывает сообщение об ошибке
        и перенаправляет на success_url.

        Args:
            request: HTTP запрос от клиента.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            HttpResponse: Ответ от родительского метода или редирект
                при возникновении ProtectedError.

        Raises:
            AttributeError: Если success_url не определен в классе.
        """
        try:
            return super().post(request, *args, **kwargs)  # noqa
        except ProtectedError:
            messages.error(request, self.protected_error_message)
            # success_url должен быть определен в дочернем классе
            if not hasattr(self, 'success_url') or self.success_url is None:
                raise AttributeError(
                    'success_url должен быть определен в классе, '
                    'использующем ProtectedErrorHandlerMixin'
                )
            return redirect(self.success_url)

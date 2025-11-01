from typing import Dict, Any, Optional

from django.http import HttpRequest
from rollbar.contrib.django.middleware import RollbarNotifierMiddleware


class CustomRollbarNotifierMiddleware(RollbarNotifierMiddleware):
    """Кастомный middleware для Rollbar с добавлением информации о пользователе."""

    def get_payload_data(
        self, request: HttpRequest, exc: Optional[Exception]
    ) -> Dict[str, Any]:
        """
        Получает дополнительные данные для отправки в Rollbar.

        Добавляет информацию о пользователе в payload, если пользователь
        авторизован.

        Args:
            request: HTTP запрос от клиента.
            exc: Исключение, если оно было вызвано.

        Returns:
            Dict[str, Any]: Словарь с данными для Rollbar. Содержит информацию
                о пользователе, если он авторизован.
        """
        payload_data: Dict[str, Any] = {}

        if not request.user.is_anonymous:
            payload_data = {
                'person': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                    'full_name': request.user.get_full_name(),
                },
            }

        return payload_data

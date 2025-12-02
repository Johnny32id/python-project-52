from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель пользователя проекта."""

    def __str__(self):
        """Возвращает строковое представление пользователя."""
        return self.get_full_name()

    def get_full_name(self) -> str:
        """
        Возвращает полное имя пользователя.

        Объединяет имя и фамилию пользователя. Если одно из полей пустое,
        возвращает только заполненное поле. Если оба поля пустые,
        возвращает username.

        Returns:
            str: Полное имя пользователя или username, если имя и фамилия
                пустые.
        """
        parts = [self.first_name, self.last_name]
        full_name = ' '.join(part for part in parts if part).strip()
        return full_name or self.username

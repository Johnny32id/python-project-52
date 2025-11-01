from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    """Модель статуса задачи."""

    name = models.CharField(
        max_length=50, verbose_name=_('Name'), unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        Возвращает строковое представление статуса.

        Returns:
            str: Название статуса.
        """
        return self.name

from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    """Модель метки задачи."""

    name = models.CharField(
        max_length=50, verbose_name=_('Name'), unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        Возвращает строковое представление метки.

        Returns:
            str: Название метки.
        """
        return self.name

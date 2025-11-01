from typing import Any, Optional

import django_filters
from django import forms
from django.db import models
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilterForm(django_filters.FilterSet):
    """Фильтр для задач."""

    labels = django_filters.ModelChoiceFilter(
        label=_('Label'),
        queryset=Label.objects.all()
    )
    self_tasks = django_filters.BooleanFilter(
        label=_('Only your tasks'),
        widget=forms.CheckboxInput,
        method='filter_by_self_tasks',
        required=False
    )

    def __init__(
        self, *args: Any, request: Optional[HttpRequest] = None, **kwargs: Any
    ) -> None:
        """
        Инициализирует фильтр с передачей request.

        Args:
            *args: Дополнительные позиционные аргументы.
            request: HTTP запрос для доступа к текущему пользователю.
            **kwargs: Дополнительные именованные аргументы.
        """
        super().__init__(*args, **kwargs)
        self.request = request

    def filter_by_self_tasks(
        self, queryset: models.QuerySet, name: str, value: bool
    ) -> models.QuerySet:
        """
        Фильтрует задачи по автору, если выбран чекбокс 'только свои задачи'.

        Args:
            queryset: Исходный QuerySet задач.
            name: Имя поля фильтра.
            value: Значение фильтра (True, если выбрано).

        Returns:
            models.QuerySet: Отфильтрованный QuerySet задач.
        """
        if (value and hasattr(self.request, 'user')
                and self.request.user.is_authenticated):
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        """Метаданные фильтра."""

        model = Task
        fields = ['status', 'executor']

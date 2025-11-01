from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import (ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  DetailView)

from task_manager.mixins import ProtectedErrorHandlerMixin


class BaseListView(LoginRequiredMixin, ListView):
    """Базовый класс для отображения списков объектов."""

    pass


class BaseCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Базовый класс для создания объектов."""

    template_name = 'create.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Добавляет контекст для универсального шаблона создания.

        Args:
            **kwargs: Дополнительные аргументы контекста.

        Returns:
            Dict[str, Any]: Словарь контекста с данными для шаблона.
        """
        context = super().get_context_data(**kwargs)
        if not hasattr(self, 'create_title'):
            context['title'] = _('Create')
        else:
            context['title'] = self.create_title
        if not hasattr(self, 'action_url'):
            # Пытаемся определить URL из имени view
            model_name = self.model._meta.verbose_name_plural.lower()
            context['action_url'] = f'{model_name}_create'
        else:
            context['action_url'] = self.action_url
        if not hasattr(self, 'button_label'):
            context['button_label'] = _('Create')
        else:
            context['button_label'] = self.button_label
        return context


class BaseUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Базовый класс для обновления объектов."""

    template_name = 'update.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Добавляет контекст для универсального шаблона обновления.

        Args:
            **kwargs: Дополнительные аргументы контекста.

        Returns:
            Dict[str, Any]: Словарь контекста с данными для шаблона.
        """
        context = super().get_context_data(**kwargs)
        if not hasattr(self, 'update_title'):
            context['title'] = _('Change')
        else:
            context['title'] = self.update_title
        if not hasattr(self, 'action_url'):
            # Пытаемся определить URL из имени view
            model_name = self.model._meta.verbose_name_plural.lower()
            context['action_url'] = f'{model_name}_update'
        else:
            context['action_url'] = self.action_url
        if not hasattr(self, 'button_label'):
            context['button_label'] = _('Change')
        else:
            context['button_label'] = self.button_label
        return context


class BaseDeleteView(LoginRequiredMixin,
                     SuccessMessageMixin,
                     ProtectedErrorHandlerMixin,
                     DeleteView):
    """Базовый класс для удаления объектов."""

    template_name = 'delete.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Добавляет контекст для универсального шаблона удаления.

        Определяет имя объекта для отображения в подтверждении удаления.

        Args:
            **kwargs: Дополнительные аргументы контекста.

        Returns:
            Dict[str, Any]: Словарь контекста с данными для шаблона.
        """
        context = super().get_context_data(**kwargs)
        if not hasattr(self, 'delete_title'):
            context['title'] = _('Deleting')
        else:
            context['title'] = self.delete_title

        # Определяем имя объекта для отображения
        obj = self.get_object()
        if hasattr(obj, 'name'):
            context['object_name'] = obj.name
        elif hasattr(obj, 'username'):
            context['object_name'] = obj.username
        elif hasattr(obj, '__str__'):
            context['object_name'] = str(obj)
        else:
            context['object_name'] = _('object')
        return context


class BaseDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    """Базовый класс для детального просмотра объектов."""

    pass

from django import forms
from django.contrib.auth import get_user_model

from task_manager.tasks.models import Task

User = get_user_model()


class TaskForm(forms.ModelForm):
    """Форма для создания и обновления задачи."""

    class Meta:
        """Метаданные формы."""

        model = Task
        fields = (
            'name',
            'description',
            'status',
            'executor',
            'labels',
        )

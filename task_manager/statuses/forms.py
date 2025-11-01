from django import forms

from task_manager.statuses.models import Status


class StatusForm(forms.ModelForm):
    """Форма для создания и обновления статуса."""

    class Meta:
        """Метаданные формы."""

        model = Status
        fields = (
            'name',
        )

from django import forms

from task_manager.labels.models import Label


class LabelForm(forms.ModelForm):
    """Форма для создания и обновления метки."""

    class Meta:
        """Метаданные формы."""

        model = Label
        fields = (
            'name',
        )

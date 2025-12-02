from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class UserForm(UserCreationForm):
    """Форма для создания и обновления пользователя."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Инициализирует форму пользователя.

        Устанавливает обязательность полей first_name и last_name.
        """
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        """Метаданные формы."""

        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        )

    def clean_username(self) -> str:
        """
        Проверяет уникальность имени пользователя.

        Returns:
            str: Очищенное имя пользователя.

        Raises:
            forms.ValidationError: Если пользователь с таким именем уже
                существует.
        """
        username = self.cleaned_data['username']
        error_message = _('A user with that username already exists.')
        if get_user_model().objects.filter(username=username).exclude(
                id=self.instance.id).exists():
            raise forms.ValidationError(error_message)
        return username

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        error_message = _('Пользователь с таким именем уже существует.')
        if get_user_model().objects.filter(username=username).exclude(
                id=self.instance.id).exists():
            raise forms.ValidationError(error_message)
        return username

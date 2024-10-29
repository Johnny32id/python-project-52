from django import forms
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Task

User = get_user_model()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'name',
            'description',
            'status',
            'executor',
            'labels',
        )
        required_fields = ('name', 'description', 'status')

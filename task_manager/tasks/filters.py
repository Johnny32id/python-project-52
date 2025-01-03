import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilterForm(django_filters.FilterSet):
    labels = django_filters.ModelChoiceFilter(label=_('Label'),
                                              queryset=Label.objects.all())
    self_tasks = django_filters.BooleanFilter(label=_('Only your tasks'),
                                              widget=forms.CheckboxInput,
                                              method='filter_by_self_tasks',
                                              required=False)

    def filter_by_self_tasks(self, queryset, author, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor']

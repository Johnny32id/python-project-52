from task_manager.tasks.models import Task


def filter_by_self_tasks(filters, request):
    if filters.get('self_tasks'):
        return Task.objects.filter(author=request.user)
    return Task.objects.all()


def filter_by_other_fields(tasks, filters):
    other_filters = {k: v for k, v in filters.items() if v and k != 'self_tasks'}
    return tasks.filter(**other_filters)


def filter_tasks(form, request):
    filters = form.cleaned_data
    tasks = filter_by_self_tasks(filters, request)
    tasks = filter_by_other_fields(tasks, filters)
    return tasks

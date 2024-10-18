from django.utils.translation import gettext_lazy as _


def navbar(request):
    """
    Provides the navbar items for the navigation bar.

    It checks if the user is authenticated and returns the corresponding
    navbar items. If the user is authenticated, it returns the links to the
    users, statuses, labels, and tasks pages. If the user is not authenticated,
    it returns the links to the login and registration pages.

    :param request: The HTTP request.
    :type request: HttpRequest
    :return: A dictionary containing the navbar items.
    :rtype: dict
    """
    user = request.user
    navbar_items = [{
        'label': _('Пользователи'),
        'url': '/users/',
        'class': 'nav-link',
        'align': ''
    }]
    if request.user.is_authenticated:
        navbar_items.append({
            'label': _('Статусы'),
            'url': '/statuses/',
            'class': 'nav-link',
            'align': ''
        })
        navbar_items.append({
            'label': _('Приветствую') + ', ' + user.username,
            'class': 'nav-link',
            'align': 'ms-auto'
        })
        navbar_items.append({
            'label': _('Выход'),
            'url': '/logout/',
            'form': True,
            'class': 'btn nav-link',
            'align': ''
        })
    else:
        navbar_items.append({
            'label': _('Вход'),
            'url': '/login/',
            'class': 'nav-link ms-auto',
            'align': 'ms-auto'
        })
        navbar_items.append({
            'label': _('Регистрация'),
            'url': '/users/create/',
            'class': 'nav-link ms-auto',
            'align': ''
        })

    return {'navbar_items': navbar_items}

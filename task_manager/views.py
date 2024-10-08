from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _


def index(request):
    return HttpResponse("Hello, world. You're at the pollapp index.")


class IndexView(TemplateView):
    template_name = "index.html"
    extra_context = {'header': _('Task manager')}

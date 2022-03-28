from django.http import HttpResponse
from django.views.generic import TemplateView

from apps.landing.models import Setup

__author__ = 'alexy'


def get_robots_txt(request):
    """
    Функция отображения robots.txt
    """
    setup = Setup.objects.filter(city__isnull=True).first()
    if setup:
        content = setup.robots_txt
    else:
        content = u'User-agent: *'
    robots_response = HttpResponse(content, content_type='text/plain')
    return robots_response


class TermsView(TemplateView):
    template_name = 'terms.html'

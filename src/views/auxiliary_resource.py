from src.views import ALLOWED_PING_USER_AGENTS, html_from

__author__ = 'mmi'

from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import render

from src.models import Article
from sublog import settings


def about_page(request):
    article = Article.objects.get(id=settings.ABOUT_ME_ID)
    return render(request, 'about.html', {'article': article})


def health_check(request):
    user_agent = request.META.get('HTTP_USER_AGENT', None)

    if user_agent not in ALLOWED_PING_USER_AGENTS:
        raise Http404
    return HttpResponse("""{ "status": "ok" }""", content_type='application/json')


def markdown_preview(request):
    source = request.POST['text']
    return HttpResponse(html_from(source), content_type='text/html')

__author__ = 'mmi'
import json

from django.http import HttpResponse
from django.http.response import Http404, HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import render

from src.views import ALLOWED_PING_USER_AGENTS, html_from, DRAFT_CACHE
from src.models import Article
from sublog import settings


def draft_endpoint(request):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    if request.method == 'GET':
        return HttpResponse(json.dumps(DRAFT_CACHE.get()))
    elif request.method == 'POST':
        return post_draft(request)
    return HttpResponseNotAllowed


def post_draft(request):
    DRAFT_CACHE.set({
        'title': request.POST['title'],
        'content': request.POST['content']
    })
    return HttpResponse(status=201)


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

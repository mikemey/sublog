__author__ = 'mmi'
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponseNotAllowed

from django.shortcuts import render, redirect

from src.models import Article
from src.views import MISSING_FIELDS_ERROR, html_from, get_post_field, ParsePostResult, DRAFT_CACHE
from sublog import settings


def new_article_page(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    if request.method == 'GET':
        return get_article_page(request)
    elif request.method == 'POST':
        return post_article(request)
    return HttpResponseNotAllowed


def get_article_page(request):
    return render(request, 'new_article.html', {'logout_target': '/'})


def post_article(request):
    parsed_post = parse_article_post(request)

    if parsed_post.error_message:
        return render(request, 'new_article.html', {
            'form_data': parsed_post.form_data,
            'error_message': parsed_post.error_message
        })

    DRAFT_CACHE.invalidate(request.user.id)
    art = parsed_post.result
    art.save()
    return HttpResponseRedirect(reverse('article', args=(art.id,)))


def parse_article_post(request):
    missing = []
    collected = {}
    title = get_post_field(request.POST, 'title', missing, collected)
    content = get_post_field(request.POST, 'content', missing, collected)

    if missing:
        error_message = MISSING_FIELDS_ERROR % ', '.join(missing)
        return ParsePostResult(None, error_message, collected)

    art = Article(
        title=title,
        content=content,
        rendered=html_from(content),
        author=request.user
    )
    return ParsePostResult(art)

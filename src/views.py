from django.core.urlresolvers import reverse

from django.http import HttpResponse

from django.http.response import HttpResponseRedirect, Http404

from django.shortcuts import render, get_object_or_404

from django.db import transaction

from django.utils.html import escape

from django.views import generic

from markdown import Markdown

from src import ARTICLES_VISIBLE
from src.models import Article, ArticleComment

MISSING_FIELDS_ERROR = 'Required field(s) missing: %s'
ALLOWED_PING_USER_AGENTS = ['UCBrowser1.0.0', 'curl/7.43.0']

MARKDOWN = Markdown()


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_articles'

    def get_queryset(self):
        return Article.objects.order_by('-pub_date')[:ARTICLES_VISIBLE]


class ArticleView(generic.DetailView):
    model = Article
    template_name = 'article.html'


def post_article(request):
    parsed_post = parse_article_post(request.POST)

    if parsed_post.error_message:
        return render(request, 'new_article.html', {
            'form_data': parsed_post.form_data,
            'error_message': parsed_post.error_message
        })

    art = parsed_post.result
    art.save()
    return HttpResponseRedirect(reverse('article', args=(art.id,)))


def health_check(request):
    user_agent = request.META.get('HTTP_USER_AGENT', None)

    if user_agent not in ALLOWED_PING_USER_AGENTS:
        raise Http404
    return HttpResponse("""{ "status": "ok" }""", content_type='application/json')


def markdown_preview(request):
    markdown = request.body
    parsed_html = MARKDOWN.convert(escape(markdown))
    return HttpResponse(parsed_html, content_type='text/html')


def post_comment(request, article_id):
    art = get_object_or_404(Article, pk=article_id)

    parsed_post = parse_comment_post(art, request.POST)

    if parsed_post.error_message:
        return render(request, 'article.html', {
            'article': art,
            'form_data': parsed_post.form_data,
            'error_message': parsed_post.error_message
        })

    store_comment(art, parsed_post.result)
    return HttpResponseRedirect(reverse('article', args=(article_id,)) + '#comments')


@transaction.atomic
def store_comment(art, article_comment):
    article_comment.save()
    art.comments_count = art.comments.count()
    art.save()


def parse_article_post(post_data):
    missing = []
    collected = {}
    title = get_post_field(post_data, 'title', missing, collected)
    content = get_post_field(post_data, 'content', missing, collected)

    if missing:
        error_message = MISSING_FIELDS_ERROR % ', '.join(missing)
        return ParsePostResult(None, error_message, collected)

    art = Article(
        title=title,
        content=content
    )
    return ParsePostResult(art)


def parse_comment_post(art, post_data):
    missing = []
    collected = {}
    name = get_post_field(post_data, 'name', missing, collected)
    email = get_post_field(post_data, 'email', missing, collected)
    content = get_post_field(post_data, 'content', missing, collected)
    title = get_post_field(post_data, 'title', missing, collected, False)

    if missing:
        error_message = MISSING_FIELDS_ERROR % ', '.join(missing)
        return ParsePostResult(None, error_message, collected)

    art_comment = ArticleComment(
        article=art,
        user_name=name,
        user_email=email,
        content=content,
        title=title
    )
    return ParsePostResult(art_comment)


def get_post_field(post_data, param, missing, collected, mandatory=True):
    if param in post_data:
        value = post_data.get(param)
        collected[param] = value
        if mandatory and (not value or value.isspace()):
            missing.append(param)
        return value

    missing.append(param)
    return None


class ParsePostResult:
    def __init__(self, result, error_message=None, form_data=None):
        self.result = result
        self.error_message = error_message
        self.form_data = form_data

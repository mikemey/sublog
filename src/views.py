from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect, Http404, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.views import generic

from markdown import Markdown

from src.models import Article, ArticleComment
from sublog import settings
from sublog.middleware.gfm_extensions import ImageLinkExtension
from sublog.settings import ARTICLES_VISIBLE

MISSING_FIELDS_ERROR = 'Required field(s) missing: %s'
ALLOWED_PING_USER_AGENTS = ['UCBrowser1.0.0', 'curl/7.43.0']

MARKDOWN = Markdown(extensions=['gfm', ImageLinkExtension()])


def html_from(markdown):
    return MARKDOWN.convert(html_escape(markdown))


def html_escape(text):
    return mark_safe(force_text(text).replace('&', '&amp;').replace('<', '&lt;')
                     .replace('>', '&gt;').replace("'", '&#39;'))


class IndexView(generic.ListView):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', {
            'latest_articles': self.get_queryset()
        })

    def get_queryset(self):
        return Article.objects.exclude(id=settings.ABOUT_ME_ID).order_by('-pub_date')[:ARTICLES_VISIBLE]


def new_article_page(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    if request.method == 'GET':
        return get_article_page(request)
    elif request.method == 'POST':
        return post_article(request)
    return HttpResponseNotAllowed


def about_page(request):
    article = Article.objects.get(id=settings.ABOUT_ME_ID)
    return render(request, 'about.html', {'article': article})


def get_article_page(request):
    return render(request, 'new_article.html', {'logout_target': '/'})


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
    source = request.POST['text']
    return HttpResponse(html_from(source), content_type='text/html')


def get_article(request, article_id):
    art = get_object_or_404(Article, pk=article_id)
    return render(request, 'article.html', {
        'article': art
    })


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
        content=content,
        rendered=html_from(content)
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
        rendered=html_from(content),
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

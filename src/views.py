import re

from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.views import generic

from src import ARTICLES_VISIBLE
from src.models import Article, ArticleComment

MISSING_FIELDS_ERROR = 'Required field(s) missing: %s'


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_articles'

    def get_queryset(self):
        return Article.objects.order_by('-pub_date')[:ARTICLES_VISIBLE]


class ArticleView(generic.DetailView):
    model = Article
    template_name = 'article.html'


class CreateArticleView(generic.CreateView):
    model = Article
    template_name = 'new_article.html'
    fields = ['title', 'content']

    def get_success_url(self):
        return reverse('article', args=(self.object.id,))


def comment(request, article_id):
    art = get_object_or_404(Article, pk=article_id)

    parsed_comment = parse_comment_post(art, request.POST)

    if parsed_comment.error_message:
        return render(request, 'article.html', {
            'article': art,
            'form_data': parsed_comment.form_data,
            'error_message': parsed_comment.error_message
        })

    store_comment(art, parsed_comment.comment)
    return HttpResponseRedirect(reverse('article', args=(article_id,)) + '#comments')


@transaction.atomic
def store_comment(art, article_comment):
    article_comment.save()
    art.comments_count = art.comments.count()
    art.save()


def parse_comment_post(art, post_data):
    missing = []
    collected = {}
    name = get_post_field(post_data, 'name', missing, collected)
    email = get_post_field(post_data, 'email', missing, collected)
    content = get_post_field(post_data, 'content', missing, collected)
    title = get_post_field(post_data, 'title', missing, collected, False)

    if missing:
        error_message = MISSING_FIELDS_ERROR % ', '.join(missing)
        return CommentResult(None, error_message, collected)

    art_comment = ArticleComment(
        article=art,
        user_name=name,
        user_email=email,
        content=(clean_content(content)),
        title=title
    )
    return CommentResult(art_comment)


def get_post_field(post_data, param, missing, collected, mandatory=True):
    if param in post_data:
        value = post_data.get(param)
        collected[param] = value
        if mandatory and (not value or value.isspace()):
            missing.append(param)
        return value

    missing.append(param)
    return None


single_newline = re.compile(r'([^\n])\n([^\n])')
single_newline_repl = r'\1\n\n\2'


def clean_content(content):
    return single_newline.sub(single_newline_repl, content)


class CommentResult:
    def __init__(self, cmt, error_message=None, form_data=None):
        self.comment = cmt
        self.error_message = error_message
        self.form_data = form_data

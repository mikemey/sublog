from django.core.exceptions import ObjectDoesNotExist

from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db import transaction

from src.service.mail_gen import notify_article_author
from src.views import get_post_field, MISSING_FIELDS_ERROR, ParsePostResult, html_from
from src.models import Article, ArticleComment


def get_article(request, article_id):
    art = get_object_or_404(Article, pk=article_id)
    prev_article = get_or_none(art.get_previous_by_pub_date)
    next_article = get_or_none(art.get_next_by_pub_date)

    return render(request, 'article.html', {
        'article': art,
        'prev_article': prev_article,
        'next_article': next_article
    })


def get_or_none(query):
    try:
        return query()
    except ObjectDoesNotExist:
        return None


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
    notify_article_author(art, parsed_post.result)
    return HttpResponseRedirect(reverse('article', args=(article_id,)) + '#comments')


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


@transaction.atomic
def store_comment(art, article_comment):
    article_comment.save()
    art.comments_count = art.comments.count()
    art.save()

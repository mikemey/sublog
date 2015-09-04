from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction

from django.views import generic

from src import ARTICLES_VISIBLE
from src.models import Article, ArticleComment


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
    success_url = '/'


def comment(request, article_id):
    art = get_object_or_404(Article, pk=article_id)
    try:
        art_comment = ArticleComment(
            article=art,
            user_name=request.POST['name'],
            user_email=request.POST['email'],
            content=request.POST['content'],
            title=request.POST.get('title', '')
        )
    except KeyError:
        return render(request, 'article.html', {
            'article': art,
            'error_message': 'Please fill in all required fields marked with an asterisk.',
        })

    store_comment(art, art_comment)
    return HttpResponseRedirect(reverse('article', args=(article_id,)))


@transaction.atomic
def store_comment(art, article_comment):
    article_comment.save()
    art.comments_count = art.comments.count()
    art.save()

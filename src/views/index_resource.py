from django.shortcuts import render
from django.views import generic

from src.models import Article
from sublog import settings
from sublog.settings import ARTICLES_VISIBLE


class IndexView(generic.ListView):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', {
            'latest_articles': self.get_queryset()
        })

    def get_queryset(self):
        return Article.objects.exclude(id=settings.ABOUT_ME_ID).order_by('-pub_date')[:ARTICLES_VISIBLE]

from django.conf.urls import url

from src.views.article_comment_resource import post_comment, get_article
from src.views.auxiliary_resource import about_page, markdown_preview, health_check, draft_endpoint
from src.views.index_resource import IndexView
from src.views.new_article_resource import new_article_page

urlpatterns = [
    url(r'^article/draft/$', draft_endpoint, name='draft'),
    url(r'^article/(?P<article_id>[0-9]+)/comment/$', post_comment, name='comment'),
    url(r'^article/(?P<article_id>[0-9]+)/$', get_article, name='article'),
    url(r'^article/$', new_article_page, name='new_article'),
    url(r'^about/$', about_page, name='about'),
    url(r'^markdown/$', markdown_preview, name='markdown'),
    url(r'^ping/$', health_check, name='ping'),
    url(r'^$', IndexView.as_view(), name='index')
]

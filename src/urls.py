from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^article/$', views.CreateArticleView.as_view(), name='new-article'),
    url(r'^article/(?P<pk>[0-9]+)/$', views.ArticleView.as_view(), name='article'),
    url(r'^article/(?P<article_id>[0-9]+)/comment/$', views.comment, name='comment'),
    url(r'^ping/$', views.health_check, name='ping'),
    url(r'^$', views.IndexView.as_view(), name='index')
]

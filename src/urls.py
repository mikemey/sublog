from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^article/(?P<article_id>[0-9]+)/comment/$', views.post_comment, name='comment'),
    url(r'^article/(?P<article_id>[0-9]+)/$', views.get_article, name='article'),
    url(r'^article/$', views.new_article_page, name='new_article'),
    url(r'^about/$', views.about_page, name='about'),
    url(r'^markdown/$', views.markdown_preview, name='markdown'),
    url(r'^ping/$', views.health_check, name='ping'),
    url(r'^$', views.IndexView.as_view(), name='index')
]

from django.db import models
from django.utils import timezone
from markupfield.fields import MarkupField


class Article(models.Model):
    content = MarkupField(markup_type='markdown', escape_html=True)
    title = models.CharField(default='', max_length=500)
    pub_date = models.DateTimeField('published', default=timezone.now)
    comments_count = models.IntegerField('# of comments', default=0)

    def sorted_comments(self):
        return self.comments.order_by('-pub_date')

    def __str__(self):
        return self.title


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, related_name='comments')
    title = models.CharField(default="", max_length=500)
    user_name = models.CharField(max_length=50)
    user_email = models.EmailField()
    pub_date = models.DateTimeField('published', default=timezone.now)
    content = MarkupField(markup_type='markdown', escape_html=True)

    def __str__(self):
        return self.title

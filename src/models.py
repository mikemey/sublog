from django.db import models
from django.db.models.fields import TextField
from django.utils import timezone


class Article(models.Model):
    title = models.CharField(default='', max_length=500)
    pub_date = models.DateTimeField('published', default=timezone.now)
    comments_count = models.IntegerField('# of comments', default=0)
    content = TextField()
    rendered = TextField()

    def sorted_comments(self):
        return self.comments.order_by('-pub_date')

    def __str__(self):
        return self.title


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, related_name='comments')
    title = models.CharField(default="", max_length=500, null=True, blank=True)
    user_name = models.CharField(max_length=50)
    user_email = models.EmailField()
    pub_date = models.DateTimeField('published', default=timezone.now)
    content = TextField()
    rendered = TextField()

    def __str__(self):
        return self.title

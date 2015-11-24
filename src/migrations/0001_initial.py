# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=500)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'published')),
                ('comments_count', models.IntegerField(default=0, verbose_name=b'# of comments')),
                ('content', models.TextField()),
                ('rendered', models.TextField()),
                ('author', models.ForeignKey(related_name='articles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=500, null=True, blank=True)),
                ('user_name', models.CharField(max_length=50)),
                ('user_email', models.EmailField(max_length=254)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'published')),
                ('content', models.TextField()),
                ('rendered', models.TextField()),
                ('article', models.ForeignKey(related_name='comments', to='src.Article')),
            ],
        ),
    ]

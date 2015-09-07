# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import markupfield.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', markupfield.fields.MarkupField(rendered_field=True)),
                ('title', models.CharField(default=b'', max_length=500)),
                ('content_markup_type', models.CharField(default=b'markdown', max_length=30, editable=False, choices=[(b'', b'--'), (b'html', 'HTML'), (b'plain', 'Plain'), (b'markdown', 'Markdown')])),
                ('_content_rendered', models.TextField(editable=False)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'published')),
                ('comments_count', models.IntegerField(default=0, verbose_name=b'# of comments')),
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
                ('content', markupfield.fields.MarkupField(rendered_field=True)),
                ('content_markup_type', models.CharField(default=b'markdown', max_length=30, editable=False, choices=[(b'', b'--'), (b'html', 'HTML'), (b'plain', 'Plain'), (b'markdown', 'Markdown')])),
                ('_content_rendered', models.TextField(editable=False)),
                ('article', models.ForeignKey(related_name='comments', to='src.Article')),
            ],
        ),
    ]

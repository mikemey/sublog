# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='_content_rendered',
            new_name='rendered',
        ),
        migrations.RemoveField(
            model_name='article',
            name='content_markup_type',
        ),
        migrations.RenameField(
            model_name='articlecomment',
            old_name='_content_rendered',
            new_name='rendered',
        ),
        migrations.RemoveField(
            model_name='articlecomment',
            name='content_markup_type',
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='articlecomment',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='article',
            name='rendered',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='articlecomment',
            name='rendered',
            field=models.TextField(),
        ),
    ]

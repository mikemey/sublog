from django.contrib import admin

from src.models import Article, ArticleComment


class ChoiceInline(admin.TabularInline):
    model = ArticleComment


class ArticleAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('title', 'pub_date', 'comments_count')
    search_fields = ['title']


admin.site.register(Article, ArticleAdmin)

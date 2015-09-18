from django.template import loader, Context

from src.email import MailSend
from src.service import sycache

mail_template = loader.get_template('partials/mail_template.html')

mail_cache = sycache.SyCache()
mck = 'mck'

email_subj_template = """New comment on article '%s'"""


def mail():
    return mail_cache.get_or_set(mck, MailSend())


def notify_article_author(art, comment):
    article_id, user_name, commenter, title = details_from(art, comment)

    email_dest = art.author.email
    email_subj = email_subj_template % title
    email_body = mail_content(article_id, user_name, commenter, title)
    mail().send(email_dest, email_subj, email_body)


def details_from(art, comment):
    author = art.author
    article_id = art.id
    user_name = author.first_name or author.username
    commenter = comment.user_name
    title = art.title
    return article_id, user_name, commenter, title


def mail_content(article_id, user_name, commenter, title):
    ctx = Context({
        'article_id': article_id,
        'username': user_name,
        'commenter': commenter,
        'title': title,
    })
    return mail_template.render(ctx)

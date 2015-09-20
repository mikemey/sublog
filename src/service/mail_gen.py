from django.template import loader, Context

from src.email import MailSend
from src.service import sycache

email_subj_template = """New comment on article '%s'"""
email_template = loader.get_template('partials/mail_template.html')

send_mail_cache = sycache.SyCache()
mck = 'mck'


def mail():
    return send_mail_cache.get_or_set(mck, MailSend())


def notify_article_author(art, comment):
    email_dest = art.author.email
    email_subj = email_subj_template % art.title
    email_body = render_email_body(with_context_from(art, comment))

    mail().send(email_dest, email_subj, email_body)


def render_email_body(ctx):
    return email_template.render(ctx)


def with_context_from(art, comment):
    username = art.author.first_name or art.author.username
    return Context({
        'article_id': art.id,
        'username': username,
        'commenter': comment.user_name,
        'title': art.title,
    })

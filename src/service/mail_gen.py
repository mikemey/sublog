from django.template import loader, Context

mail_template = loader.get_template('partials/mail_template.html')


def generate_mail_content(user_name, commenter, title):
    ctx = Context({
        'username': user_name,
        'commenter': commenter,
        'title': title,
    })
    return mail_template.render(ctx)

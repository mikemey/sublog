from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from markdown import Markdown

from src.service.sycache import SyCache
from sublog.middleware.gfm_extensions import ImageLinkExtension

MISSING_FIELDS_ERROR = 'Required field(s) missing: %s'
ALLOWED_PING_USER_AGENTS = ['UCBrowser1.0.0', 'curl/7.43.0']

MARKDOWN = Markdown(extensions=['gfm', ImageLinkExtension()])

DRAFT_CACHE = SyCache({'title': '', 'content': ''})


def html_from(markdown):
    return MARKDOWN.convert(html_escape(markdown))


def html_escape(text):
    return mark_safe(force_text(text).replace('&', '&amp;').replace('<', '&lt;')
                     .replace('>', '&gt;').replace("'", '&#39;'))


def get_post_field(post_data, param, missing, collected, mandatory=True):
    if param in post_data:
        value = post_data.get(param)
        collected[param] = value
        if mandatory and (not value or value.isspace()):
            missing.append(param)
        return value

    missing.append(param)
    return None


class ParsePostResult:
    def __init__(self, result, error_message=None, form_data=None):
        self.result = result
        self.error_message = error_message
        self.form_data = form_data

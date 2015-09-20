__author__ = 'mmi'

import re

TITLE_1 = 'title 1'
CONTENT_1 = 'content 1'
EXP_CONTENT_1 = '<p>content 1</p>'

TITLE_2 = 'title 2'
CONTENT_2 = 'content 2'
EXP_CONTENT_2 = '<p>content 2</p>'

NEW_TITLE = 'new title'
NEW_CONTENT = 'new content'
EXP_NEW_CONTENT = '<p>new content</p>'

USER_NAME_1 = 'user 1'
USER_NAME_2 = 'user 2'

article_title_re = re.compile('"panel-title">([^<]*)</h3>')
article_content_re = re.compile("""<div class="article_content markdown-body">(.+?(?=</div))""", re.DOTALL)


def get_articles(response):
    titles = re_list(article_title_re, response.content)
    contents = re_list(article_content_re, response.content)

    articles = []
    ix = 0
    for title in titles:
        articles.append({
            'title': title,
            'content': (contents[ix])
        })
        ix += 1
    return articles


comment_title_re = re.compile('"panel-title">([^<]*)</h4>')
comment_name_re = re.compile('list-group-item">([^<]*)<span')
comment_content_re = re.compile('<!--comment-content-start-->\s*<div class="panel-body markdown-body">'
                                '(.+?(?=</div>\s*<!--comment-content-end-->))', re.DOTALL)


def get_comments(response):
    titles = re_list(comment_title_re, response.content)
    names = re_list(comment_name_re, response.content)
    contents = re_list(comment_content_re, response.content)

    comments = []
    ix = 0
    for title in titles:
        comments.append({
            'title': title,
            'name': names[ix],
            'content': contents[ix]
        })
        ix += 1
    return comments


version_no_re = re.compile("""="version">([^<]*)<""")


def get_version(response):
    return find_or_none(version_no_re, response)


article_id_re = re.compile(r'/article/(\d*)/')


def get_article_id(article_page):
    return find_or_none(article_id_re, article_page)


error_message_re = re.compile(""""alert">([^<]*)""")


def get_error_message(response):
    return find_or_none(error_message_re, response)


user_name_re = re.compile("""<span id="user">([^<]*)""")


def get_user_name(response):
    return find_or_none(user_name_re, response)


def find_or_none(find_re, response):
    search = find_re.search(response.content)
    if search:
        return search.group(1)
    return None


def re_list(regex, content):
    result = []
    for found_title in regex.findall(content):
        result.append(found_title.strip())

    return result


about_title_re = re.compile('about-title">([^<]*)</h3>')
about_content_re = re.compile("""about-content markdown-body">(.+?(?=</div))""", re.DOTALL)


def about_me_content(response):
    return {'title': find_or_none(about_title_re, response),
            'content': find_or_none(about_content_re, response)
            }


toc_re = re.compile("""\s<a href="[^"]*">(.+?(?=</a))""", re.DOTALL)


def get_toc(response):
    raw_toc_list = re_list(toc_re, response.content)
    toc_list = [extract_toc(toc_entry) for toc_entry in raw_toc_list]
    return toc_list


def extract_toc(toc_entry):
    toc_entry = toc_entry.strip()
    is_active = '\n\n' in toc_entry.replace(' ', '')
    if is_active:
        label = toc_entry.split('\n')[0]
    else:
        label = toc_entry
    return {'label': label, 'is_active': is_active}


prev_link_re = re.compile("""class="previous" href="([^"]*)">([^<]*)""")
next_link_re = re.compile("""class="next" href="([^"]*)">([^<]*)""")


def get_previous_link(response):
    return get_link(prev_link_re, response)


def get_next_link(response):
    return get_link(next_link_re, response)


def get_link(link_re, response):
    search = link_re.search(response.content)
    if search:
        return {'href': search.group(1),
                'label': search.group(2)}
    return None

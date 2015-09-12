import re

article_title_re = re.compile('"panel-title">([^<]*)</h3>')
article_content_re = re.compile("""<div class="article_content">(.+?(?=</div))""", re.DOTALL)


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
comment_content_re = re.compile('div class="panel-body"><p>([^<]*)</p>')


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


def re_list(regex, content):
    result = []
    for found_title in regex.findall(content):
        result.append(found_title.strip())

    return result


version_no_re = re.compile("""="version">([^<]*)<""")


def get_version(response):
    version_no = re_list(version_no_re, response.content)
    return version_no[0]

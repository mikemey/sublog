from src.models import Article, ArticleComment

# a1 = Article.objects.get(pk=1)
# a2 = Article.objects.get(pk=2)
# a3 = Article.objects.get(pk=3)
# a4 = Article.objects.get(pk=4)
# a5 = Article.objects.get(pk=5)

# comments = ArticleComment.objects.all()
# for com in comments:
#     com.content = com.content.raw
#     com.save()

def save_article(title, pub_date, content, comments_count, author_id='xyz'):
    ar = Article(
        content=content,
        title=title,
        pub_date=pub_date,
        comments_count=comments_count,
        author=author_id
    )
    ar.save()
    return ar


def save_comment(art, title, name, email, date, content):
    com = ArticleComment(
        article=art,
        title=title,
        user_name=name,
        user_email=email,
        pub_date=date,
        content=content
    )
    com.save()
    return


a1 = save_article('First post', '2015-09-04 11:31:16', 'Ladida', '1')
a2 = save_article('second post', '2015-09-04 11:32:04', 'huahuuasdfhdsahf', '1')
a3 = save_article('third', '2015-09-04 11:32:37',
                  '### lala \n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. \n\n Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ### ut labore et dolore \n\n magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n ### this is the end.',
                  '6')
a4 = save_article('fourht', '2015-09-04 11:35:11',
                  'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n##another header\n Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                  '14')
a5 = save_article('last post', '2015-09-04 11:38:45',
                  'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                  '3')

save_comment(a1, 'so awesome', 'me', 'bla@blu.com', '2015-09-04 11:31:16',
             '# very important ## also important #### not so important')
save_comment(a2, 'buuuhh', 'fad', 'ds@fda.com', '2015-09-04 11:32:04', 'comment on ### article 2')
save_comment(a3, 'dasfdsa', 'asdfasd', 'adsfa@sdfa.com', '2015-09-04 11:32:37', 'comment on ### article 3')
save_comment(a3, 'adsf  a fds dsa fdsa f dsa', 'dasg b araf adea dsafds ', 'adsfa@sdfa.com', '2015-09-04 11:32:37',
             'comment on ### article 3')
save_comment(a3, 'dasf adafd af dsaf dfg a', ' adsfdsaf a da fa d  ', 'adsfa@sdfa.com', '2015-09-04 11:32:37',
             'comment on ### article 3')
save_comment(a3, 'adfs fasads sad', 'asdfasd', 'adsfa@sdfa.com', '2015-09-04 11:32:37', 'comment on ### article 3')
save_comment(a3, 'adf adsfasd f ', 'dasfa sfda', 'adsfa@sdfa.com', '2015-09-04 11:32:37', 'comment on ### article 3')
save_comment(a3, 'adsf af f f sda', 'adsf  dasf', 'adsfa@sdfa.com', '2015-09-04 11:32:37', 'comment on ### article 3')
save_comment(a4, 'adsf', 'asdf', 'bbbb@caad.com', '2015-09-04 11:35:11', 'comment on ### article 4')
save_comment(a4, 'byjbyjdb', 'bdyj', 'bbbb@caad.com', '2015-09-04 11:35:11', 'comment on ### article 4')
save_comment(a4, 'jbbyj', 'jdbyjdytb', 'bbbb@caad.com', '2015-09-04 11:35:11', 'comment on ### article 4')
save_comment(a4, 'bydjyj', 'byrubjy', 'bbbb@caad.com', '2015-09-04 11:35:11', 'comment on ### article 4')
save_comment(a4, 'fsdgfds', 'gtrytuby', 'bbbb@caad.com', '2015-09-04 11:35:11', 'comment on ### article 4')
save_comment(a4, 'fdsgfdgsd', 'dfghhdfghdfghgf fgdsfsdgfg', 'bbbb@caad.com', '2015-09-04 11:35:11',
             'comment on ### article 4')
save_comment(a4, 'ghhjgjhjf', 'fujyjgh', 'bbbb@caad.com', '2015-09-04 11:36:30', 'comment on ### article 4')
save_comment(a4, 'ufjuuf', 'fjfun', 'bbbb@caad.com', '2015-09-04 11:36:31', 'comment on ### article 4')
save_comment(a4, 'yjfju', 'juyjf', 'bbbb@caad.com', '2015-09-04 11:36:32', 'comment on ### article 4')
save_comment(a4, 'dsafsadf', 'fdsadfarb', 'bbbb@caad.com', '2015-09-04 11:36:34', 'comment on ### article 4')
save_comment(a4, 'sdfsa', 'sdfsf', 'bbbb@caad.com', '2015-09-04 11:36:35', 'comment on ### article 4')
save_comment(a4, 'bdyhyydjb', 'dtjydtjbdj', 'bbbb@caad.com', '2015-09-04 11:38:02', 'comment on ### article 4')
save_comment(a4, 'bhdtyhbtyhby', 'dsafdbr', 'bbbb@caad.com', '2015-09-04 11:38:02', 'comment on ### article 4')
save_comment(a4, 'ttdgtjbjd', 'strnrd', 'bbbb@caad.com', '2015-09-04 11:38:02', 'comment on ### article 4')
save_comment(a5, '3333333', 'dfasvfv', 'asdfas@bfdala.com', '2015-09-04 11:38:45', 'comment on ### article 5')
save_comment(a5, '22222222', 'fsadagrg', 'asdfas@bfdala.com', '2015-09-04 11:38:45', 'comment on ### article 5')
save_comment(a5, '11111111', 'abrbara', 'asdfas@bfdala.com', '2015-09-04 11:38:45', 'comment on ### article 5')

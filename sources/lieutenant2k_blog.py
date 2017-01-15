from urllib.error import URLError
from urllib.request import urlopen

import lxml.html as lh

from sources.checker import Checker


class Lieutenant2kBlogChecker(Checker):
    def __init__(self):
        self.last_post = None
        self.tags = ['алгебра', 'институт', 'сессия', 'студенты',
                     'фпм', 'работа', 'анекдот', 'диплом']

    def __str__(self):
        return 'Lieutenant2k blog'

    def get_changes(self):
        changes = []
        posts = []
        got_data = False
        timeouts = [10, 20, 30, 50]

        for timeout in timeouts:
            try:
                doc = lh.parse(urlopen(
                    'http://lieutenant2k.livejournal.com/', timeout=timeout))
                got_data = True
                break
            except URLError as error:
                print(error, 'timeout:', timeout)

        if got_data:
            raw_posts = doc.xpath('//div[@class="asset-inner"]')

            for post in raw_posts:
                header = post.find_class("subj-link")
                name = header[0].text_content()
                link = header[0].values()[0]

                try:
                    posts_tags = post.find_class("asset-tags-list")[0]\
                        .text_content()
                except IndexError:
                    posts_tags = ''

                for tag in self.tags:
                    if tag in posts_tags:
                        posts.append({'name': name,
                                      'link': link})
                        break

            if posts:
                for post in posts:
                    if post['link'] == self.last_post:
                        break
                    else:
                        changes.append(('Lieutenant2k posted "{}"'.format(
                            post['name']), post['link']))
                self.last_post = posts[0]['link']

            return changes

        return 'Cannot get data from source'

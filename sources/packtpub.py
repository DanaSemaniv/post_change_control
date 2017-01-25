import lxml.html as lh

from urllib.error import URLError
from urllib.request import urlopen

from sources.checker import Checker
from settings import (
    error_message,
    timeouts,
    packtpub_interval,
)


class PacktpubChecker(Checker):
    def __init__(self):
        self.interval = packtpub_interval
        self.last_check = None

        self.last_book = None
        self.link = 'https://www.packtpub.com/packt/offers/free-learning/'

    def __str__(self):
        return 'Packtpub'

    def get_changes(self):
        got_data = False

        for timeout in timeouts:
            try:
                doc = lh.parse(urlopen(self.link, timeout=timeout))
                got_data = True
                break
            except URLError as error:
                print(error, 'timeout:', timeout)

        if got_data:
            book_title = doc.xpath(
                '//div[@class="dotd-title"]')[0].text_content().strip()

            if book_title != self.last_book:
                message = 'There is new book: ' + book_title
                self.last_book = book_title
                return [(message, self.link)]
            else:
                return

        return error_message

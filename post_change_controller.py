import datetime
import time

import vk

from sources.checker import Checker
from settings import (
    error_message,
    sleep_time,
)
from access_token import token


class Observer:
    def __init__(self):
        self.sources = []
        self.session = vk.AuthSession(access_token=token)
        self.vk_api = vk.API(self.session)

    def add_source(self, source):
        if isinstance(source, Checker):
            self.sources.append(source)
        else:
            print('Cannot add {} object. It must be a subclass of '
                  'Checker'.format(source))

    def send_messages(self, changes):
        for change in changes:
            for messages in change:
                for message in messages:
                    self.vk_api.messages.send(domain='id85601111',
                                              message=message)
                print(
                    'message "{}" sent at {}'.format(
                        messages, datetime.datetime.now()))

    def check_for_changes(self):
        while True:
            sources = []
            now = datetime.datetime.now()
            for source in self.sources:
                if not source.last_check or \
                    now - source.last_check > datetime.timedelta(
                            seconds=source.interval):
                    sources.append(source)

            changes = []
            for source in sources:
                change = source.get_changes()
                source.last_check = now
                if change:
                    if change == error_message:
                        print(error_message, source)
                    else:
                        changes.append(change)
            if changes:
                try:
                    self.send_messages(changes)
                except vk.exceptions.VkException as exception:
                    print(exception)
                    self.notify_about_problem()
            else:
                print('nothing changed')
            print('sleeping...')
            time.sleep(sleep_time)

    def notify_about_problem(self):
        try:
            self.vk_api.messages.send(domain='id85601111',
                                      message='There are some problems with '
                                              'your parser. Check it!')
        except vk.exceptions.VkException:
            pass

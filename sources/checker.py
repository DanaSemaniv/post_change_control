from abc import ABCMeta, abstractmethod


class Checker(metaclass=ABCMeta):

    @abstractmethod
    def get_changes(self):
        pass

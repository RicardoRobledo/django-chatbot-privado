from abc import ABC


__author__ = 'Ricardo'
__version__ = '0.1'


class BaseScrapper(ABC):

    @classmethod
    def get_template(self):
        pass

    @classmethod
    def get_a_tags(self):
        pass

    @classmethod
    def get_text(self):
        pass

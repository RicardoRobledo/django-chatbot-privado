from django.conf import settings
from string import Template

from requests_html import HTMLSession

from .base_scrapper import BaseScrapper


__author__ = 'Ricardo'
__version__ = '0.1'


__all__ = ['BcsGobScrapper']


template = """
//hacer
Analiza el trámite y contesta mis dudas, si hago referencia a un formato o enlace mandamelo. Si pregunto por
algo de información que no existe o un enlace, dime que no se cuenta con eso.

//tramite
$text
"""


class BcsGobScrapper(BaseScrapper):
    """
    This class give information about sat's web page
    """

    def __init__(self, url):

        # getting response
        self.__response = HTMLSession().get(url)


    def get_a_tags(self):
        pass


    def get_text(self):
        
        texts = self.__response.html.find('main', first=True).text

        return texts


    def get_template(self, text, a_tags):
        """
        This method format our template

        :param text: text of the web page
        :param a_tags: a list with 'a' tags
        :return: a string being a template with formatted text
        """

        formatted_template = Template(template).substitute(
            text=text,
            a_tags=str.join('', a_tags)
        )

        return formatted_template

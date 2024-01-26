from django.conf import settings
from string import Template

from requests_html import HTMLSession
from bs4 import BeautifulSoup

from .base_scrapper import BaseScrapper


__author__ = 'Ricardo'
__version__ = '0.1'


__all__ = ['AppsBCSScrapper']


template = """
//hacer
cuando se te pregunte de información de este servicio o trámite indica que no contamos con información directa,
pero puede consultarla en el sitio web del portal público del gobierno de baja california sur, dale el enlace en una etiqueta '<a href=enlace>servicio</a>'

//servicio
$text

//formatos y enlaces
$a_tags
"""


class AppsBCSScrapper(BaseScrapper):
    """
    This class dig in the structure of apps bcs's web content to get information
    """

    def __init__(self, url):

        # getting response
        self.__response = HTMLSession().get(url)

        # getting text in html format
        #self.__soup = BeautifulSoup(self.__response.html.html, 'html.parser')


    def get_a_tags(self):
        pass


    def get_text(self):
        pass


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

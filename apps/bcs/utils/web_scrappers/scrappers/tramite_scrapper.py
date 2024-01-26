from django.conf import settings
from string import Template

from requests_html import HTMLSession

from .base_scrapper import BaseScrapper


__author__ = 'Ricardo'
__version__ = '0.1'


__all__ = ['TramiteScrapper']


template = """
//hacer
cuando se te pregunte de información de este servicio o tramite indica que no contamos con información directa,
pero puede consultarla en el sitio web de tramites y catalogos del gobierno de baja california sur, dale el enlace en una etiqueta '<a href=enlace>servicio</a>'

//servicio o tramite
$text

//formatos y enlaces
$a_tags
"""


class TramiteScrapper(BaseScrapper):
    """
    This class dig in the structure of tramite's web content to get information
    """

    def __init__(self, url):

        # getting response
        #self.__response = HTMLSession().get(url)
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

    def get_a_tags(self):
        pass

    def get_text(self):
        pass

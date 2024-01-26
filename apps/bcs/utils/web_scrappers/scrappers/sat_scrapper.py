from django.conf import settings
from string import Template

from .base_scrapper import BaseScrapper


__author__ = 'Ricardo'
__version__ = '0.1'


__all__ = ['SatScrapper']


template = """
//hacer
cuando se te pregunte de información de este servicio indica que no contamos con información directa,
pero puede consultarla en el sitio web del SAT, dale el enlace en una etiqueta '<a href=enlace>servicio</a>'

//servicio
$text

//formatos y enlaces
$a_tags
"""


class SatScrapper(BaseScrapper):
    """
    This class give information about sat's web page
    """

    def __init__(self, url):

        # getting response
        self.__response = url


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

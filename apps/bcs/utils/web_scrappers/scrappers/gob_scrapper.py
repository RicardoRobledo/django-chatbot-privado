from django.conf import settings
from string import Template
import re

from requests_html import HTMLSession
from bs4 import BeautifulSoup

from .base_scrapper import BaseScrapper


__author__ = 'Ricardo'
__version__ = '0.1'


__all__ = ['GobScrapper']


template = """
//hacer
Analiza el trámite y contesta mis dudas, si hago referencia a un formato o enlace mandamelo. Si pregunto por
algo de información o un enlace que no existe, dime que no se cuenta con eso.

si pregunto por un enlace para hacer trámites en línea y no se indica uno, contesta que no se cuenta con eso.

//tramite
$text
                                   
//formatos y enlaces:
$a_tags
"""


class GobScrapper(BaseScrapper):
    """
    This class give information about gob's web page
    """

    def __init__(self, url):

        # getting response
        self.__response = HTMLSession().get(url)

        # getting text in html format
        self.__soup = BeautifulSoup(self.__response.html.html, 'html.parser')


    def delete_invalid_a_tags(self, a_tags):

        for index, a_tag in enumerate(a_tags):

            href = a_tag.attrs['href']
            
            if href[len(href)-4:]=='.jsp':
                del a_tags[index]

        return a_tags


    def get_a_tags(self):

        section_tag = self.__response.html.find('#9448')[1]
        a_tags = self.delete_invalid_a_tags(section_tag.find('a'))

        return a_tags


    def get_text(self):
        
        texts = self.__soup.find_all('section')[2].stripped_strings
        text = str.join('\n', texts)

        return re.sub(r'\s+', ' ', text)


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

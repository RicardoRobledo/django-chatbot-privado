from django.conf import settings
from string import Template

from requests_html import HTMLSession
from bs4 import BeautifulSoup

from .base_scrapper import BaseScrapper


__author__ = 'Ricardo'
__version__ = '0.1'


__all__ = ['TramiteServicioScrapper']


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


class TramiteServicioScrapper(BaseScrapper):
    """
    This class dig in the structure of tramites y servicios's web content to get information
    """

    def __init__(self, url):

        # getting response
        self.__response = HTMLSession().get(url)

        # getting text in html format
        self.__soup = BeautifulSoup(self.__response.html.html, 'html.parser')
    

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
    

    def format_hrefs(self, a_tags):
        """
        This method prefix incomplete urls

        :param a_tags: a list with 'a' tags
        :return: 'a' tags with complete prefixes
        """

        for a_tag in a_tags:

            href = a_tag.attrs["href"]
            
            if href.startswith('/'):
                a_tag.attrs["href"] = f'{settings.TRAMITES_Y_SERVICIOS_URL}{href[1:]}'
        
        return a_tags


    def get_a_tags(self):

        div_container_tag = self.__soup.find_all('div', class_='container')[1]
        a_breadcrumbs_tag = div_container_tag.find('div', class_='breadcrumbs')

        if a_breadcrumbs_tag:
            a_breadcrumbs_tag.extract()

        a_tags = div_container_tag.find_all('a')
        a_tags = self.format_hrefs(a_tags)

        return a_tags


    def get_text(self):

        # become in html to get texts
        texts = self.__soup.find_all('div', class_='container')[1].stripped_strings

        return str.join('\n', texts)

from django.conf import settings
from string import Template

from requests_html import HTMLSession
from .base_scrapper import BaseScrapper


__author__ = 'Ricardo'
__version__ = '0.1'


__all__ = ['CatalogoNacionalScrapper']


template = """
//hacer
Analiza el trámite y contesta mis dudas, si hago referencia a un formato o enlace mandamelo. Si pregunto por
algo de información que no existe dime que no se cuenta con eso.

si pregunto por algún enlace que no está indicado en los formatos y enlaces dime que no se cuenta con ello.

//tramite
$text
                                   
//formatos y enlaces:
$a_tags
"""


class CatalogoNacionalScrapper(BaseScrapper):
    """
    This class dig in the structure of catalogo nacional's web content to get information
    """

    def __init__(self, url):
        self.__response = HTMLSession().get(url)
    

    def delete_invalid_a_tags(self, a_tags):

        for index, a_tag in enumerate(a_tags):

            href = a_tag.attrs['href']
            
            if href=='#' or href=='' or href=='/cdn-cgi/l/email-protection':
                del a_tags[index]

        return a_tags

    
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


    def delete_duplicated_a_tags(self, a_tags):

        unique_hrefs = []
        set_unique_hrefs = set()

        for tag in a_tags:

            href = tag.attrs['href']

            if (href not in set_unique_hrefs):
                set_unique_hrefs.add(href)
                unique_hrefs.append(tag)
    
        return unique_hrefs
    

    def format_hrefs(self, a_tags):
        """
        This method prefix incomplete urls

        :param a_tags: a list with 'a' tags
        :return: 'a' tags with complete prefixes
        """

        for a_tag in a_tags:

            href = a_tag.attrs["href"]
            
            if href.startswith('/'):
                a_tag.attrs["href"] = f'{settings.CATALOGO_NACIONAL_URL}{href[1:]}'
        
        return a_tags


    def get_a_tags(self):

        # getting 'a' tags in aside tag
        a_tags_aside = self.__response.html.find('aside', first=True).find('div', first=True).find('a')
        a_tags_aside = self.delete_invalid_a_tags(self.format_hrefs(a_tags_aside))

        # getting 'a' tags in main container
        a_tags_main_container = self.__response.html.find('#contenedorPrincipal', first=True).find('#collapseDivsBody', first=True).find('a')
        a_tags_main_container = self.format_hrefs(self.delete_invalid_a_tags(self.delete_duplicated_a_tags(a_tags_main_container)))

        return a_tags_aside + a_tags_main_container


    def get_text(self):

        # getting text
        text = self.__response.html.find('#contenedorPrincipal', first=True).text

        return text

from django.conf import settings

from bs4 import BeautifulSoup
import requests

from .cleaners import clean_tags
from .scrappers.catalogo_nacional_scrapper import CatalogoNacionalScrapper
from .scrappers.tramite_servicio_scrapper import TramiteServicioScrapper
from .scrappers.apps_bcs_scrapper import AppsBCSScrapper
from .scrappers.tramite_scrapper import TramiteScrapper
from .scrappers.bcs_gob_scrapper import BcsGobScrapper
from .scrappers.sat_scrapper import SatScrapper
from .scrappers.gob_scrapper import GobScrapper


__author__ = 'Ricardo'
__version__ = '0.1'


__all__ = ['BCSScrapper']


class BCSScrapper():
    """
    This class retrieve information about baja california sur's web page through web scrapping
    """

    def __init__(self):
        pass


    def get_web_content(self, url):

        # getting data
        response = requests.get(url)

        # getting web content
        return BeautifulSoup(response.text, 'html.parser')


    # ----------------------------------------------------
    #                getters of information
    # ----------------------------------------------------


    def get_bcs_list_procedures(self):
        """
        This method get all the procedures in a web page

        :return: a list with dictionaries about texts and hrefs
        """

        web_content = self.get_web_content(settings.BCS_SERVICES_URL)

        tags = [tag for tag in web_content.body.find('div', id='primary').find_all('a')]

        # cleaning web content
        cleaned_tags = clean_tags(tags)

        # formatting web content in json
        data = [
            {'text':text, 'href':href}
            for text, href in zip(cleaned_tags[0], cleaned_tags[1])
        ]

        return data


    def get_bcs_procedure(self, index):
        """
        This method get a procedure in a web page and give us its web content

        :return: a list with dictionaries about texts and hrefs
        """

        # getting list procedures
        list_procedures = self.get_bcs_list_procedures()

        # getting data of procedure
        #
        #{
        #    'text':'abc...',
        #    'href':'https://...'
        #}
        procedure = list_procedures[int(index)]

        #print(procedure)
        #print(procedure['href'])

        url = procedure['href']
        template = ''
        a_tags = []
        text = ''

        # getting web content
        #
        # options:
        # 1 - catalogo nacional
        # 2 - tramites y servicios
        # 3 - sat
        # 4 - tramites
        # 5 - apps3.bcs
        # 6 - bcs.gob
        # 7 - gob.mx
        if(url.startswith(settings.CATALOGO_NACIONAL_URL)):

            catalogo_nacional_scrapper = CatalogoNacionalScrapper(url)

            a_tags = [
                f"{a_tag.text}->{a_tag.attrs['href']}"
                for a_tag in catalogo_nacional_scrapper.get_a_tags()
            ]
            
            text = catalogo_nacional_scrapper.get_text()
            template = catalogo_nacional_scrapper.get_template(text, a_tags)
        
        elif(url.startswith(settings.TRAMITES_Y_SERVICIOS_URL)):
            
            tramite_servicio_scrapper = TramiteServicioScrapper(url)

            a_tags = [
                f"{a_tag.text} -> {a_tag.attrs['href']},\n"
                for a_tag in tramite_servicio_scrapper.get_a_tags()
            ]

            text = tramite_servicio_scrapper.get_text()
            template = tramite_servicio_scrapper.get_template(text, a_tags)
        
        elif(url.startswith(settings.SAT_URL)):

            sat_scrapper = SatScrapper(url.replace('https', 'http'))
            template = sat_scrapper.get_template(
                'Servicio de Administración Tributaria (SAT)',
                [f'sitio web del SAT -> {url}']
            )
        
        elif(url.startswith(settings.TRAMITES_URL)):

            tramite_scrapper = TramiteScrapper(url)
            
            #a_tags = tramite_scrapper.get_a_tags()
            #text = tramite_scrapper.get_text()

            template = tramite_scrapper.get_template(
                procedure['text'],
                [f'sitio web de tramites y catalogos del gobierno de baja california sur -> {url}']
            )
        
        elif(url.startswith(settings.APPS_BCS_URL) or 
             url.startswith(settings.CITAS_LINEA_URL)
             or url.startswith(settings.APPS_BCS_URL.replace('https', 'http'))):

            apps_bcs_scrapper = AppsBCSScrapper(url)

            template = apps_bcs_scrapper.get_template(
                procedure['text'],
                [f'portal publico del gobierno de baja california sur -> {url}']
            )
        
        elif(url.startswith(settings.BCS_GOB_URL)):

            bcs_gob_scrapper = BcsGobScrapper(f'{url}archivo-general-estado/anuencias/')

            text = bcs_gob_scrapper.get_text()
            template = bcs_gob_scrapper.get_template(text, [''])
        
        elif(url.startswith(settings.GOB_URL)):

            gob_scrapper = GobScrapper(url)

            a_tags = [
                f"{a_tag.text} -> {a_tag.attrs['href']},\n"
                for a_tag in gob_scrapper.get_a_tags()
            ]

            text = gob_scrapper.get_text()
            template = gob_scrapper.get_template(text, a_tags)


        return template

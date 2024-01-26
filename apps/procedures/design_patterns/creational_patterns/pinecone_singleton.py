from django.conf import settings
import time

from langchain_community.vectorstores import Pinecone as VSPinecone
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone

from ...utils.cleaners.format_cleaners import clean_format


__author__ = 'Ricardo'
__version__ = '0.1'


class PineconeSingleton():


    __client = None
    __embeddings = None


    @classmethod
    def __get_connection(self):
        """
        This method create our client
        """

        client = Pinecone().Index("tramites")

        return client


    def __new__(cls, *args, **kwargs):
        
        if cls.__client==None:

            # making connection
            cls.__client = cls.__get_connection()
            cls.__embeddings = OpenAIEmbeddings()
        
        return cls.__client
    

    @classmethod
    async def create(cls):
        import pandas as pd
        df = pd.read_csv("data.csv")

        urls = []
        texts = df["Texts"].to_list()
        titles = df["Titles"].to_list()

        for i in df["Urls"].to_list():

            url = []
            
            for j in i.split(','):

                url.append(j.split('->'))
            
            urls.append(url)

        title_new = []

        from ...models import Procedure, ProcedureURL

        for i in titles:

            import re

            pattern = r"[áéíóú]"
            accents = {
                'á': 'a',
                'é': 'e',
                'í': 'i',
                'ó': 'o',
                'ú': 'u'
            }
            title_new.append(re.sub(pattern, lambda x: accents[x.group()], i).replace(' ', '-'))
        
        from asgiref.sync import sync_to_async

        for i, u in zip(title_new, urls):
            obj = await sync_to_async(list)(Procedure.objects.filter(title=i))

            for j in u:
                print(j)
                await ProcedureURL.objects.acreate(description=j[0], url=j[1], procedure_id=obj[0])
            print()
            print()
    

    @classmethod
    async def search_similarity_procedure(cls, text:str, title:str):
        """
        This method search the similarity in a text given inside Pinecone

        :param text: an string beging our text to query
        :param title: our namespace in which our Pinecone has chunks
        :return: a list with our documents 
        """

        vspinecone = VSPinecone.from_existing_index('tramites', cls.__embeddings)
        docs = await vspinecone.asimilarity_search(text, k=4, namespace=clean_format(title))
        
        return docs
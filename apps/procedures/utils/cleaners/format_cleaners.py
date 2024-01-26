import re


__author__ = 'Ricardo'
__version__ = '0.1'


def clean_format(title:str):
    """
    This method clean the format given to put in one allowed by Pinecone and referenced in our database

    :param title: string that represents a title of a procedure
    :return: a string being a title formatted
    """

    pattern = r"[áéíóú]"
    accents = {
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u'
    }
    
    return re.sub(pattern, lambda x: accents[x.group()], title)

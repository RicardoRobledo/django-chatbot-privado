from ...procedures.models import Procedure

from asgiref.sync import sync_to_async


__author__ = 'Ricardo'
__version__ = '0.1'


class BCSRepository():
    """
    This class retrieve information about baja california sur's web page
    """

    async def get_bcs_list_procedures(self):

        procedures = await sync_to_async(list)(Procedure.objects.all())
        procedures = [{'text':procedure.title.replace('-', ' ')} for procedure in procedures]

        return procedures

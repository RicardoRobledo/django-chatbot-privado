#from asgiref.sync import sync_to_async

from rest_framework.response import Response
from adrf.decorators import api_view as async_apy_view

from ..repositories.bcs_repository import BCSRepository


__author__ = 'Ricardo'
__version__ = '0.1'


#@sync_to_async
@async_apy_view(['GET'])
async def get_bcs_list_procedures(request):

    bsc_repository = BCSRepository()
    data = await bsc_repository.get_bcs_list_procedures()

    return Response(data)

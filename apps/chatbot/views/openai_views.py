from django.conf import settings
import json
from asgiref.sync import sync_to_async

from rest_framework.response import Response
from rest_framework.decorators import api_view
from adrf.decorators import api_view as async_api_view

from ..repositories.openai_repository import OpenAIRepository
from ..desing_patterns.creational_patterns.singleton.openai_singleton import OpenAISingleton
#from ...bcs.utils.web_scrappers.scrapper import BCSScrapper
#from ..desing_patterns.behavioral_design_patterns.state.conversation_flow import ConversationFlow
from ...procedures.design_patterns.creational_patterns.pinecone_singleton import PineconeSingleton

from ...procedures.utils.prompt_handlers.prompt_procedure import format_prompt
from ...procedures.models import Procedure, ProcedureURL
from ...procedures.utils.cleaners.format_cleaners import clean_format


@async_api_view(['POST'])
async def post_message(request):
    """
    This view post a message
    """

    # getting request data
    query_dict = request.data
    array_chat_str = query_dict.get('array_chat', '')
    thread_id = query_dict.get('thread_id', '')
    title = query_dict.get('title', '').replace(' ', '-')

    # become in json
    # {
    #    'role': 'user',
    #    'content': 'abc...'
    # }
    array_chat_json = json.loads(array_chat_str)

    # getting chunks in vectorial database
    PineconeSingleton()
    docs = await PineconeSingleton.search_similarity_procedure(array_chat_json['content'], title)
    docs = map(lambda doc:doc.page_content, docs)
    context = str.join('', docs)

    # getting urls from database
    procedure = Procedure.objects.filter(title=title)
    procedure = await procedure.afirst()
    urls = ProcedureURL.objects.filter(procedure_id=procedure.id)

    formatted_urls = []

    async for url in urls:
        formatted_urls.append(f"{url.description} -> {url.url}") # giving format to urls

    message = format_prompt(context, formatted_urls, array_chat_json['content'])

    #await ProcedureSingleton.create()
    #template_procedure = BCSScrapper().get_bcs_procedure(request.data.get('index'))

    # linking user message with procedure content
    #array_chat_json['content'] = f"{template_procedure}\n//duda\n{array_chat_json['content']}"

    # making conversation flow
    #conversation_flow = ConversationFlow()
    #conversation_flow.send_message(array_chat_json, thread_id)
    
    OpenAISingleton()
    openai_repository = OpenAIRepository()
    msg = await openai_repository.post_user_message(message, thread_id)

    return Response({'msg':msg})


@api_view(['POST'])
def post_clean(request):
    """
    This view close our connection
    """

    OpenAISingleton.close_connection(request.data.get('thread_id'))

    return Response({})


@api_view(['POST'])
def post_create_thread(request):
    """
    This view create a thread
    """

    OpenAISingleton()
    thread = OpenAIRepository().post_create_thread()

    return Response({'thread_id':thread.id})

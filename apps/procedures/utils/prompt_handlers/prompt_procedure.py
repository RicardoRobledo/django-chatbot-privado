from langchain.prompts import PromptTemplate


__author__ = 'Ricardo'
__version__ = '0.1'


def format_prompt(context:str, urls:list, question:str):

    prompt_file_path = 'apps/procedures/prompts/prompt_procedure.txt'
    template = ''

    with open(prompt_file_path, 'r', encoding="utf-8") as archivo:
        template = archivo.read()

    return PromptTemplate.from_template(template).format(procedure=context, urls=str.join('\n', urls), question=question)

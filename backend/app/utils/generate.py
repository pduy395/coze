from helper.llm import Gemini, GPT, LocalLLM
from typing import List
from schemas.message import MessageResponse, MessageBase
from datetime import datetime

async def generate_answer(
    instruction: str,
    chats: List[dict],
    context: str,
    question: str,
    config_llm: dict,
    websocket
):
    llm_name = config_llm['llm_name']
    if llm_name[:6] != 'gemini':
        if (llm_name[:3] == 'gpt'):
            model = GPT(instruction=instruction,
                        model_name=config_llm['llm_name'],
                        temperature=config_llm['temperature'],
                        top_p=config_llm['top_p'],
                        frequency_penalty=config_llm['frequency_penalty'],
                        presence_penalty=config_llm['presence_penalty'],
                        max_length=config_llm['max_length'],
                        output_format=config_llm['output_format'])
        else:
            model = LocalLLM(instruction=instruction,
                        model_name=config_llm['llm_name'],
                        temperature=config_llm['temperature'],
                        top_p=config_llm['top_p'],
                        frequency_penalty=config_llm['frequency_penalty'],
                        presence_penalty=config_llm['presence_penalty'],
                        max_length=config_llm['max_length'],
                        output_format=config_llm['output_format'])
        messages = model.get_messages(question, chats, context)
        response = await model.invoke(messages, question, websocket)
        return response
        

    else:
        model = Gemini(instruction=instruction,
                       model_name=config_llm['llm_name'],
                       temperature=config_llm['temperature'],
                       top_p=config_llm['top_p'],
                       max_length=config_llm['max_length'],
                       output_format=config_llm['output_format']
                       )
        
        messages = model.get_messages(question, chats, context)
        response = await model.invoke(messages, question, websocket)
        return response
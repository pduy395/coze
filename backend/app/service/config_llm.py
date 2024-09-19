import repository.config_llm
from fastapi import Depends
from repository.config_llm import ConfigLLMDBSupabase, ConfigLLMDBPostgreSql


config_llm_db = ConfigLLMDBPostgreSql()

async def get_config_llm (
    chatbot_id: int,
    name: str,
    session: Depends
):
    config_llm = await config_llm_db.get_config_llm_by_chatbot_id_and_label(chatbot_id, name, session)
    
    if config_llm['config_type'] == 'precise':
        config_llm['temperature'] = 1
        config_llm['top_p'] = 1
        config_llm['frequency_penalty'] = 0
        config_llm['presence_penalty'] = 0

    elif config_llm['config_type'] == 'balance':
        config_llm['temperature'] = 0.5
        config_llm['top_p'] = 1
        config_llm['frequency_penalty'] = 0
        config_llm['presence_penalty'] = 0

    elif config_llm['config_type'] == 'creative':
        config_llm['temperature'] = 0.8
        config_llm['top_p'] = 1
        config_llm['frequency_penalty'] = 0
        config_llm['presence_penalty'] = 0

    return config_llm
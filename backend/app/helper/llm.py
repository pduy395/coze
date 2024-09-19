import google.generativeai as genai
from google.generativeai import GenerationConfig
from openai import OpenAI
import os
from dotenv import load_dotenv
from schemas.message import MessageBase 
from datetime import datetime, timezone
import tiktoken
import subprocess
import asyncio


def count_tokens(text: str, model_name: str = "gpt-4o") -> int:
    encoding = tiktoken.encoding_for_model(model_name)
    tokens = encoding.encode(text)
    return len(tokens)

load_dotenv()

class LLM:
    def __init__(self, instruction, model_name='gemini-1.5-pro', temperature=0.5, top_p=1, frequency_penalty=0, presence_penalty=0, max_length=1024, output_format='text'):
        self.instruction = instruction
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.max_length = max_length
        self.output_format = output_format
    
    def get_history(self, chats):
        pass
     
    def get_prompt(self, context, question):
        # question= "\n\"\"\"" + question + "\"\"\"",
        if context == "----":
            prompt =  f'{question}'
            return prompt
        else: 
            prompt = f'''
知識、提供された情報、メッセージ履歴に基づいて、次の質問に答えてください。
提供された情報:{context}
質問: {question}
答え: '''
            return prompt



class Gemini(LLM):
    def __init__(self, instruction, model_name='gemini-1.5-flash', temperature=0.7, top_p=0.5, frequency_penalty=0, presence_penalty=0, max_length=1024, output_format='text'):
        super().__init__(instruction, model_name, temperature, top_p, frequency_penalty, presence_penalty, max_length, output_format)
        self.safety_settings =  [
            {
                'category': 'HARM_CATEGORY_HARASSMENT',
                'threshold': 'BLOCK_NONE'
            },
            {
                'category': 'HARM_CATEGORY_HATE_SPEECH',
                'threshold': 'BLOCK_NONE'
            },
            {
                'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
                'threshold': 'BLOCK_NONE'
            },
            {
                'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
                'threshold': 'BLOCK_NONE'
            }
        ]
        google_api_key = os.environ['GOOGLE_API_KEY']   
        genai.configure(api_key=google_api_key)
        if (instruction != ''): 
            self.model = genai.GenerativeModel(model_name=self.model_name, 
                                               safety_settings=self.safety_settings, 
                                               system_instruction=self.instruction)
        else: 
            self.model = genai.GenerativeModel(model_name=self.model_name, 
                                               safety_settings=self.safety_settings)
        if self.output_format == 'json':
            self.config = GenerationConfig(
                temperature=temperature,
                top_p=top_p,
                max_output_tokens=max_length,
                response_mime_type="application/json"
            )
        else:
            self.config = GenerationConfig(
                temperature=temperature,
                top_p=top_p,
                max_output_tokens=max_length
            )
    
    def get_history(self, chats):
        history = []
        for chat in chats:
            history.append({'role': 'user', 'parts': [chat['question']]})
            history.append({'role': 'model', 'parts': [chat['answer']]})
        return history
    
    def get_messages(self, question, chats, context):
        messages = self.get_history(chats)
        prompt = self.get_prompt(context, question)
        messages.append({'role': 'user', 'parts': [prompt]})
        # print (messages)
        return messages

    async def invoke(self, messages, question, websocket):
        response = self.model.generate_content(contents=messages, generation_config=self.config, stream=True)
        answer = ''
        for chunk in response:
            await asyncio.sleep(0.0001)
            await websocket.send_json({'data':chunk.text,
                                       'input_tokens':chunk.usage_metadata.prompt_token_count,
                                       'output_tokens':chunk.usage_metadata.candidates_token_count})
            answer += chunk.text
            last_chunk = chunk
       
        message = MessageBase(
            question=question,
            answer=answer,
            input_tokens=last_chunk.usage_metadata.prompt_token_count,
            output_tokens=last_chunk.usage_metadata.candidates_token_count,
            time=datetime.now(timezone.utc).astimezone()
        )
        
        return message

class GPT(LLM):
    def __init__(self,instruction, model_name='gpt-4o-mini', temperature=0.5, top_p=1, frequency_penalty=0, presence_penalty=0, max_length=1024, output_format='text'):
        super().__init__(instruction, model_name, temperature, top_p, frequency_penalty, presence_penalty, max_length, output_format)
        openai_api_key = os.environ.get('OPENAI_API_KEY')
        self.client = OpenAI(api_key=openai_api_key)
        if output_format == 'json':
            self.instruction += '\nDesigned to output JSON'

    def get_history(self, chats):
        history = []
        for chat in chats:
            history.append({'role': 'user', 'content': chat['question']})
            history.append({'role': 'assistant', 'content': chat['answer']})
        return history
    
    def get_messages(self, question, chats, context):
        if self.instruction != '':
            messages = [{'role': 'system', 'content': self.instruction}]
        else:
            messages = []
        history = self.get_history(chats)
        messages.extend(history)
        prompt = self.get_prompt(context, question)
        messages.append({'role': 'user', 'content': prompt})

        return messages
    
    async def invoke(self, messages, question, websocket):
        if self.output_format == 'json':
            response = self.client.chat.completions.create (
                model=self.model_name,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
                top_p=self.top_p,
                temperature=self.temperature,
                max_tokens=self.max_length,
                messages=messages,
                response_format={'type':'json_object'},
                stream=True
            )
            
        else:
            response = self.client.chat.completions.create (
                model=self.model_name,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
                top_p=self.top_p,
                temperature=self.temperature,
                max_tokens=self.max_length,
                messages=messages,
                stream=True
            )
        answer = ""
        if "gpt" in self.model_name:
            in_tokens = count_tokens(str(messages), model_name=self.model_name)
        else:
            in_tokens = count_tokens(str(messages))
        out_tokens=0
        for chunk in response:
            if chunk.choices[0].delta.content == None:
                message = MessageBase(
                    question=question,
                    answer= answer,
                    input_tokens=in_tokens,
                    output_tokens=out_tokens,
                    time=datetime.now(timezone.utc).astimezone()
                )
                break
            out_tokens += 1 
            answer += chunk.choices[0].delta.content
            await asyncio.sleep(0.0001)
            await websocket.send_json({'data': chunk.choices[0].delta.content,
                                       'input_tokens': in_tokens,
                                       'output_tokens': out_tokens})

        return message
                        

class LocalLLM(GPT):
        def __init__(self,instruction, model_name, temperature=0.5, top_p=1, frequency_penalty=0, presence_penalty=0, max_length=1024, output_format='text'):
            super().__init__(instruction, model_name, temperature, top_p, frequency_penalty, presence_penalty, max_length, output_format)
            llm_studio_key = os.environ.get('LLM_STUDIO_KEY')
            self.client = OpenAI(base_url="http://192.168.1.7:5678/v1", api_key=llm_studio_key)
            if instruction == '':
                self.instruction = 'You are a helpful, smart, kind, and efficient AI assistant. You always fulfill the user\'s requests to the best of your ability.\n'
        
        def get_history(self, chats):
            history = []
            for chat in chats:
                history.append({'role': 'user', 'content': chat['question']})
                if chat['answer'] != '':
                    history.append({'role': 'assistant', 'content': chat['answer']})
            return history 
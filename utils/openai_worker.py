from config import Configuration

import openai
import tiktoken

import asyncio

openai.api_key = Configuration.openai_token


class AIWorker:

    chat_model = "gpt-3.5-turbo"
    audio_model = "whisper-1"
    tokens_limit = 4096

    @staticmethod
    async def gpt(messages):
        answer = 'Упс.. Щось пішло не так в запиті до ChatGPT. Будь ласка, спробуйте ще раз'
        try:
            response = await openai.ChatCompletion.acreate(
                engine=AIWorker.chat_model,
                messages=messages,
                temperature=0.7,
                max_tokens=800,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )
        except openai.error.APIConnectionError as e:
            print(f"An error occurred while calling OpenAI API: {e}")
        else:
            if 'choices' in response and len(response['choices']) > 0:
                answer = response['choices'][0]['message']['content']
        return answer

    @staticmethod
    async def whisper(media_bytes):
        def __transcribe__():
            response = openai.Audio.transcribe(AIWorker.audio_model, media_bytes)["text"]
            if "text" in response:
                return response["text"]

        loop = asyncio.get_event_loop()
        transcript = await loop.run_in_executor(None, __transcribe__)

        return transcript

    @staticmethod
    def count_text_tokens(text):
        encoding = tiktoken.encoding_for_model(AIWorker.chat_model)
        num_tokens = len(encoding.encode(text))
        return num_tokens

    @staticmethod
    def count_context_tokens(context):
        num_tokens = 0
        for message in context:
            num_tokens += AIWorker.count_text_tokens(message["content"])
        return num_tokens



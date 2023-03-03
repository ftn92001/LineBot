import requests
from LineBot.settings import OPEN_AI_API_KEY

def call_completions(content):
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPEN_AI_API_KEY}'
        },
        json = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': content}],
            'temperature': 0.6,
            'max_tokens': 3000
        }
    )

    return response.json()['choices'][0]['message']['content'].replace('\n',' ')
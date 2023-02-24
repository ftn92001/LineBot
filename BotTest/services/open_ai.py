import requests
from LineBot.settings import OPEN_AI_API_KEY

def call_completions(prompt):
    response = requests.post(
        'https://api.openai.com/v1/completions',
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPEN_AI_API_KEY}'
        },
        json = {
            'model': 'text-davinci-003',
            'prompt': prompt,
            'temperature': 0.6,
            'max_tokens': 300
        }
    )

    return response.json()['choices'][0]['text'].replace('\n',' ')
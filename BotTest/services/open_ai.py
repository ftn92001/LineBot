import requests
from LineBot.settings import OPEN_AI_API_KEY

prev_content = ''
prev_answer = ''

def call_completions(content):
    global prev_content
    global prev_answer
    messages = [
        {'role': 'user', 'content': prev_content},
        {'role': 'user', 'content': prev_answer},
        {'role': 'user', 'content': content},
    ]
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPEN_AI_API_KEY}'
        },
        json = {
            'model': 'gpt-3.5-turbo',
            'messages': messages,
            'temperature': 0.6,
            'max_tokens': 3000
        }
    )
    answer = response.json()['choices'][0]['message']['content']

    prev_content = content
    prev_answer = answer
    print(response.json())
    return answer.replace('\n',' ')

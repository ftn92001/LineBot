import requests
from LineBot.settings import GEMINI_API_KEY

prev_content = ''
prev_answer = ''

def generate_content(content):
    global prev_content
    global prev_answer
    contents = [
        {'role': 'user', 'parts': [{ 'text': prev_content }]},
        {'role': 'model', 'parts': [{ 'text': prev_answer }]},
        {'role': 'user', 'parts': [{ 'text': content }]},
    ]
    response = requests.post(
        f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}',
        headers = {
            'Content-Type': 'application/json',
        },
        json = {
            "contents": contents
        }
    )
    answer = response.json()['candidates'][0]['content']['parts'][0]['text']

    prev_content = content
    prev_answer = answer
    print(response.json())
    return answer

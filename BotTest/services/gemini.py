import requests
from LineBot.settings import GEMINI_API_KEY

prev_content = ''
prev_answer = ''

def generate_content(content, image_content=None):
    global prev_content
    global prev_answer
    if image_content:
        contents = [
            {
                "role": "user",
                "parts": [
                    { "text": content },
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_content
                        }
                    }
                ]
            }
        ]
    else:
        contents = [
            {"role": "user", "parts": [{ "text": prev_content }]},
            {"role": "model", "parts": [{ "text": prev_answer }]},
            {"role": "user", "parts": [{ "text": content }]}
        ]

    model = "gemini-flash-lite-latest"
    response = requests.post(
        f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}',
        headers = {
            'Content-Type': 'application/json',
        },
        json = {
            "contents": contents
        }
    )
    print(response.json())
    answer = response.json()['candidates'][0]['content']['parts'][0]['text']

    prev_content = content
    prev_answer = answer
    return answer

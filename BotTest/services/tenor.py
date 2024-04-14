import requests
from LineBot.settings import TENOR_API_KEY

def get_gif_imgs(content):
    imgs = []
    texts = []
    urls = []

    r = requests.get(
        f"https://tenor.googleapis.com/v2/search?key={TENOR_API_KEY}&client_key=LINEBOT&q={content}&limit=50&media_filter=gif"
    )

    if r.status_code == 200:
        results = r.json()['results']
        for result in results:
            imgs.append(result['media_formats']['gif']['url'])
            texts.append(result['title'])
            urls.append(result['url'])
    else:
        results = None
    return imgs, texts, urls

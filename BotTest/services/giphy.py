import requests
from LineBot.settings import GIPHY_API_KEY

GIPHY_SEARCH_URL = "https://api.giphy.com/v2/search"

def get_gif_imgs(content, limit=25):
    imgs = []
    texts = []
    urls = []

    r = requests.get(
        GIPHY_SEARCH_URL,
        params={
            "key": GIPHY_API_KEY,
            "client_key": "LINEBOT",
            "q": content,
            "limit": limit,
            "media_filter": "gif",
        },
    )

    if r.status_code == 200:
        results = r.json().get('results', [])
        for result in results:
            imgs.append(result['media_formats']['gif']['url'])
            texts.append(result['title'])
            urls.append(result['url'])
    return imgs, texts, urls

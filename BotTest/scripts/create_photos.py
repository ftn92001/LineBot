import requests
from bs4 import BeautifulSoup
from BotTest.models import Photo

PTT_URL = 'https://www.ptt.cc'

def create_beauty_imgs():
    imgs = []
    # 從上次更新到的頁數開始
    current_page = get_web_page(f"{PTT_URL}/bbs/Beauty/index4000.html")
    current_articles, next_url = get_articles(current_page)
    updated_objs = []
    created_objs = []
    datas = Photo.objects.all()
    exist = False
    while True:
        for article in current_articles:
            url = PTT_URL + article['href']
            this_page = get_web_page(url)
            if this_page is None:
                continue
            img_name = article['title']
            imgs.extend(get_img(this_page))
            if imgs:
                print(img_name) 
            for img in imgs:
                defaults = {"image_src": img, "name": img_name, "url": url}
                for data in datas:
                    if data.image_src == img:
                        obj = data
                        exist = True
                        break
                if exist:
                    for key, value in defaults.items():
                        setattr(obj, key, value)
                    updated_objs.append(obj)
                else:
                    obj = Photo(image_src = img, name = img_name, url = url)
                    created_objs.append(obj)
                exist = False
            imgs = []
        if next_url == '/bbs/Beauty/index.html':
            break
        Photo.objects.bulk_update(updated_objs, ['image_src', 'name', 'url'])
        Photo.objects.bulk_create(created_objs)
        updated_objs = []
        created_objs = []
        print(f"更新#{next_url}")
        next_page = get_web_page(PTT_URL + next_url)
        try_times = 10
        while try_times > 0 and next_page is None:
            next_page = get_web_page(PTT_URL + next_url)
            try_times -= 1
        current_articles, next_url = get_articles(next_page)
    

def get_web_page(url):
    resp = requests.get(
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code == 200:
        return resp.text
    print('Invalid url:', resp.url)
    return None


def get_articles(dom):
    soup = BeautifulSoup(dom, 'html5lib')

    paging_div = soup.find('div', 'btn-group btn-group-paging')
    next_url = paging_div.find_all('a')[2]['href'] if paging_div.find_all('a')[2].has_key('href') else '/bbs/Beauty/index.html'

    articles = []
    divs = soup.find_all('div', 'r-ent')
    for div in divs:
        if '正妹' in div.find('div', 'title').text and div.find('a'):
            href = div.find('a')['href']
            title = div.find('a').text
            author = div.find('div', 'author').text if div.find('div', 'author') else ''
            articles.append({
                'title': title,
                'href': href,
                'author': author
            })

    return articles, next_url

def get_img(page):
    soup = BeautifulSoup(page, 'html5lib')
    hrefs = soup.find_all('a')
    return [href['href'] for href in hrefs if ('https://i.imgur.com/' in href['href'] and len(href['href']) < 100)]

def run():
    create_beauty_imgs()

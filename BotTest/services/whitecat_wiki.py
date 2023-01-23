import requests
from bs4 import BeautifulSoup
import json
from copy import deepcopy
from linebot.models import FlexSendMessage

def character_info():
    url  = "https://shironekoproject.fandom.com/zh/wiki/%E4%BE%9D%E7%99%BB%E5%A0%B4%E6%99%82%E9%96%93"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all('div', class_='mw-lookuptable-item', limit=12)
    file = json.load(open('BotTest/services/whitecat.json','r',encoding='utf-8'))
    template = file['contents'][0]
    for _ in range(11):
        file['contents'].append(deepcopy(template))

    for i in range(len(items)):
        content = file['contents'][i]['body']['contents']
        src_template = content[2]
        name_template = content[3]
        
        b = items[i].find_all('b')
        title = b[0].text
        time = b[1].text
        content[0]['text'] = title
        content[1]['text'] = time
        
        characters = items[i].find_all('a')
        for j in range(len(characters)):
            uri = f"https://shironekoproject.fandom.com{characters[j]['href']}"
            img = characters[j].find('img')
            src = img.get('data-src') or img['src']
            name = img['alt'].split('s.png')[0]
            if j != 0:
                content.append(deepcopy(src_template))
                content.append(deepcopy(name_template))
            content[2*(j+1)]['action']['uri'] = uri
            content[2*(j+1)]['contents'][0]['url'] = src
            content[2*(j+1)+1]['contents'][0]['text'] = name
    return file

def character_info_template_message():
    message = character_info()
    return FlexSendMessage(alt_text='白貓角色資訊', contents=message)

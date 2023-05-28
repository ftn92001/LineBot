import requests
from bs4 import BeautifulSoup
from linebot.models import TextSendMessage

def anime(query):
    r = requests.get(f"https://anime1.me/{query}") #將網頁資料GET下來
    soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
    #season = soup.select_one("h2.entry-title") #取HTML標中的 <h2 class="entry-title"></h2> 中的<h2>標籤存入season
    temps = soup.select("td") #取HTML標中的 td 標籤存入temp
    names = []

    for temp in temps:
        name = temp.find("a")
        if name:
            names.append(name.text)
    del names[-1]
    StrName = "\n".join(names)
    return TextSendMessage(text=StrName)
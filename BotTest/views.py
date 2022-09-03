from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from googletrans import Translator
from linebot.models.send_messages import ImageSendMessage
import requests as req
from bs4 import BeautifulSoup
import random

# Create your views here.
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
yt_api = settings.GOOGLE_API_KEY
 

@csrf_exempt
def callback(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')
    try:
        events = parser.parse(body, signature)  # 傳入的事件
    except InvalidSignatureError:
        return HttpResponseForbidden()
    except LineBotApiError:
        return HttpResponseBadRequest()
    for event in events:
        if isinstance(event, MessageEvent):
            text = event.message.text # 傳進來的訊息
            img = ''
            source_user = event.source.user_id
            #source_group = event.source.group_id
            print(source_user)
            #print(source_group)
            if text[:2] in ['!p', '！p', '!P', '！P']:
                img = get_image(text[2:])
            elif text[:3].lower() in ['!yt', '！yt']:
                text = get_video(text[3:])
            elif text[:2] == '@中':
                text = translation(text[2:], 'zh-tw')
            elif text[:2] == '@英':
                text = translation(text[2:], 'en')
            elif text[:2] == '@日':
                text = translation(text[2:], 'ja')
            elif text[:2] == '@韓':
                text = translation(text[2:], 'ko')
            elif text[:3] in ['!遊戲', '！遊戲']:
                # !遊戲 3000 200 10 5
                #   0    1   2   3  4
                global moneys
                moneys = text.split(' ')
                moneys = moneys[1:]
                text = '輸入"!抽"進行'
            elif text[:2] in ['!抽', '！抽']:
                text = random.choice(moneys)
                moneys.remove(text)
            elif ['美金', 'USD', 'usd'] in text:
                price = get_price('usd', text)
                text = get_currency('usd', price)
            elif ['日元', '日幣', 'JPY', 'jpy'] in text:
                price = get_price('jpy', text)
                text = get_currency('jpy', price)
            elif ['港元', '港幣', 'HKD', 'hkd'] in text:
                price = get_price('hkd', text)
                text = get_currency('hkd', price)
            elif ['韓元', 'KRW', 'krw'] in text:
                price = get_price('krw', text)
                text = get_currency('krw', price)
            elif ['人民幣', 'CNY', 'cny'] in text:
                price = get_price('cny', text)
                text = get_currency('cny', price)
            else:
                continue
            if not img:
                # 回復文字 ， text='要傳的訊息'
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text = text)) 
            else:
                # 回復圖片 ， original_content_url='要傳的圖片' preview_image_url='要傳的圖片預覽'
                print(img)
                line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url = img, preview_image_url = img)) 

    return HttpResponse()

def translation(text, dest):
    transtor = Translator()
    return transtor.translate(text, dest).text
    
def get_image(str):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'}
    url = f'https://www.google.com.tw/search?tbm=isch&q={str}'
    response = req.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    imgs = soup.find_all('img')
    src = []
    for img in imgs:
        if s := img.get('data-src'):
            src.append(s)
    return random.choice(src)

def get_video(str):
    url = f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&type=video&order=viewCount&q={str}&key={yt_api}'
    response = req.get(url)
    data = response.json()
    v = data['items'][0]['id']['videoId']
    return f'https://www.youtube.com/watch?v={v}'

def get_price(currency, text):
    match currency:
        case ('usd'):
            for i in ['美金', 'USD']:
                text.replace(i, 'usd')
            rindex = text.index('usd')
            i = rindex - 1
            while (not (text[i: rindex].is_digit() or text[i] == '.')):
                i -= 1
            return float(text[i + 1:rindex])
        case ('jpy'):
            for i in ['日元', '日幣', 'JPY']:
                text.replace(i, 'jpy')
            rindex = text.index('jpy')
            i = rindex - 1
            while (not (text[i: rindex].is_digit() or text[i] == '.')):
                i -= 1
            return float(text[i + 1:rindex])
        case ('hkd'):
            for i in ['港元', '港幣', 'HKD']:
                text.replace(i, 'hkd')
            rindex = text.index('hkd')
            i = rindex - 1
            while (not (text[i: rindex].is_digit() or text[i] == '.')):
                i -= 1
            return float(text[i + 1:rindex])
        case ('krw'):
            for i in ['韓元', 'KRW']:
                text.replace(i, 'krw')
            rindex = text.index('krw')
            i = rindex - 1
            while (not (text[i: rindex].is_digit() or text[i] == '.')):
                i -= 1
            return float(text[i + 1:rindex])
        case ('cny'):
            for i in ['人民幣', 'CNY']:
                text.replace(i, 'cny')
            rindex = text.index('cny')
            i = rindex - 1
            while (not (text[i: rindex].is_digit() or text[i] == '.')):
                i -= 1
            return float(text[i + 1:rindex])
        
def get_currency(currency, price):
    url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
    response = req.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    trs = soup.find_all('tr')
    match currency:
        case ('usd'):
            for tr in trs:
                if '美金 (USD)' in tr.find_all('div')[2].text:
                    return f"{price}美金(USD) = {price * float(tr.find_all('td')[2])} 新台幣(TWD)"    
        case ('jpy'):
            for tr in trs:
                if '日元 (JPY)' in tr.find_all('div')[2].text:
                    return f"{price}日元(JPY) = {price * float(tr.find_all('td')[2])} 新台幣(TWD)"
        case ('hkd'):
            for tr in trs:
                if '港幣 (HKD)' in tr.find_all('div')[2].text:
                    return f"{price}港幣(HKD) = {price * float(tr.find_all('td')[2])} 新台幣(TWD)"
        case ('krw'):
            for tr in trs:
                if '韓元 (KRW)' in tr.find_all('div')[2].text:
                    return f"{price}韓元(KRW) = {price * float(tr.find_all('td')[2])} 新台幣(TWD)"
        case ('cny'):
            for tr in trs:
                if '人民幣 (CNY)' in tr.find_all('div')[2].text:
                    return f"{price}人民幣(CNY) = {price * float(tr.find_all('td')[2])} 新台幣(TWD)"
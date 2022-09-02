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
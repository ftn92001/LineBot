from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage, TemplateSendMessage, ImageCarouselTemplate, ImageCarouselColumn, MessageAction

from googletrans import Translator
import requests as req
from bs4 import BeautifulSoup
import random
import datetime

from .services.ptt_beauty import get_beauty_imgs
from .services.user_money import raise_money, reduce_money
from .models import LineUser, DailyAttendance

# Create your views here.
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
yt_api = settings.GOOGLE_API_KEY
usd = ['美金', 'USD', 'usd']
jpy = ['日圓', '日元', '日幣', 'JPY', 'jpy']
hkd = ['港幣', '港元', '港圓', 'HKD', 'hkd']
krw = ['韓元', '韓圓', 'KRW', 'krw']
cny = ['人民幣', 'CNY', 'cny']
 
def home_view(request):
    image_src, image_name = get_beauty_imgs(1)
    return render(request, "index.html", {
        "image_src": image_src,
        "image_name": image_name,
    })

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
            imgs = []
            texts = []
            source_user = event.source.user_id
            #source_group = event.source.group_id
            print(source_user)
            #print(source_group)
            user = LineUser.objects.get_or_create(line_id = source_user, defaults={"line_id": source_user, "money": 0})[0]
            if text[:3] in ['!簽到', '！簽到']:
                daily_attendance = user.daily_attendance
                last_daily_attendance = daily_attendance.latest('id').time if daily_attendance.exists() else None
                if  last_daily_attendance is None or last_daily_attendance.date() != datetime.date.today():
                    DailyAttendance.objects.create(line_user = user)
                    raise_money(user, 50)
                    texts = [f"成功簽到，你有{user.money}顆石頭"]
                else:
                    texts = ['今天已經簽到過了']
            elif text[:3] in ['!石頭', '！石頭']:
                texts = [f"你還有{user.money}顆石頭"]
            elif text[:3] in ['!正妹', '！正妹'] or text[:5] in ['!抽女朋友', '！抽女朋友']:
                if user.money >= 1:
                    imgs, texts = get_beauty_imgs(1)
                    reduce_money(user, 1)
                else:
                    texts = [f"你的石頭不足，剩下{user.money}顆石頭"]
            elif text[:4] in ['!十連抽', '！十連抽']:
                if user.money >= 10:
                    imgs, texts = get_beauty_imgs(10)
                    reduce_money(user, 10)
                else:
                    texts = [f"你的石頭不足，剩下{user.money}顆石頭"]
            elif text[:3] in ['!北捷', '！北捷']:
                imgs = ['https://web.metro.taipei/pages/assets/images/routemap2020.png']
            elif text[:3] in ['!中捷', '！中捷']:
                imgs = ['https://www.tmrt.com.tw/static/img/metro-life/map/map.jpg']
            elif text[:3] in ['!高捷', '！高捷']:
                imgs = ['https://www.krtc.com.tw/Content/userfiles/images/guide-map.jpg?v=c24_1']
            elif text[:2] in ['!p', '！p', '!P', '！P']:
                imgs = [get_image(text[2:])]
            elif text[:3].lower() in ['!yt', '！yt']:
                texts = [get_video(text[3:])]
            elif text[:2] == '@中':
                texts = [translation(text[2:], 'zh-tw')]
            elif text[:2] == '@英':
                texts = [translation(text[2:], 'en')]
            elif text[:2] == '@日':
                texts = [translation(text[2:], 'ja')]
            elif text[:2] == '@韓':
                texts = [translation(text[2:], 'ko')]
            elif text[:3] in ['!遊戲', '！遊戲']:
                # !遊戲 3000 200 10 5
                #   0    1   2   3  4
                global moneys
                moneys = text.split(' ')
                moneys = moneys[1:]
                texts = ['輸入"!抽"進行']
            elif text[:2] in ['!抽', '！抽']:
                if moneys:
                    text = random.choice(moneys)
                    moneys.remove(text)
                else:
                    text = '已抽完，輸入"!遊戲 xx xx"重新進行'
                texts = [text]
            elif any(currency in text for currency in usd):
                price = get_price('usd', text)
                texts = [get_currency('usd', price)]
            elif any(currency in text for currency in jpy):
                price = get_price('jpy', text)
                texts = [get_currency('jpy', price)]
            elif any(currency in text for currency in hkd):
                price = get_price('hkd', text)
                texts = [get_currency('hkd', price)]
            elif any(currency in text for currency in krw):
                price = get_price('krw', text)
                texts = [get_currency('krw', price)]
            elif any(currency in text for currency in cny):
                price = get_price('cny', text)
                texts = [get_currency('cny', price)]
            else:
                continue
            
            if len(imgs) == 10 and len(texts) == 10:
                # 回復多張圖片
                image_carousel_template_message = TemplateSendMessage(
                    alt_text='ImageCarousel template',
                    template=ImageCarouselTemplate(
                        columns=[
                            ImageCarouselColumn(
                                image_url=imgs[0],
                                action=MessageAction(
                                    label='1',
                                    text=f"1.{texts[0]}"
                                ),
                            ),
                            ImageCarouselColumn(
                                image_url=imgs[1],
                                action=MessageAction(
                                    label='2',
                                    text=f"2.{texts[1]}"
                                ),
                            ),
                            ImageCarouselColumn(
                                image_url=imgs[2],
                                action=MessageAction(
                                    label='3',
                                    text=f"3.{texts[2]}"
                                ),
                            ),
                            ImageCarouselColumn(
                                image_url=imgs[3],
                                action=MessageAction(
                                    label='4',
                                    text=f"4.{texts[3]}"
                                ),
                            ),
                            ImageCarouselColumn(
                                image_url=imgs[4],
                                action=MessageAction(
                                    label='5',
                                    text=f"5.{texts[4]}"
                                ),
                            ),
                            ImageCarouselColumn(
                                image_url=imgs[5],
                                action=MessageAction(
                                    label='6',
                                    text=f"6.{texts[5]}"
                                ),
                            ),
                            ImageCarouselColumn(
                                image_url=imgs[6],
                                action=MessageAction(
                                    label='7',
                                    text=f"7.{texts[6]}"
                                ),
                            ),
                            ImageCarouselColumn(
                                image_url=imgs[7],
                                action=MessageAction(
                                    label='8',
                                    text=f"8.{texts[7]}"
                                ),
                            ),
                            ImageCarouselColumn(
                                image_url=imgs[8],
                                action=MessageAction(
                                    label='9',
                                    text=f"9.{texts[8]}"
                                ),
                            ),
                            ImageCarouselColumn(
                                image_url=imgs[9],
                                action=MessageAction(
                                    label='10',
                                    text=f"10.{texts[9]}"
                                ),
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token, image_carousel_template_message)
            else:
                msgs = []
                # 回復圖片 ， original_content_url='要傳的圖片' preview_image_url='要傳的圖片預覽'
                if imgs:
                    msgs.extend(ImageSendMessage(original_content_url=img, preview_image_url=img) for img in imgs)
                # 回復文字 ， text='要傳的訊息'
                if texts:
                    msgs.extend(TextSendMessage(text = text) for text in texts)
                line_bot_api.reply_message(event.reply_token, msgs)
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
            for i in usd:
                text = text.replace(i, 'usd')
            rindex = text.find('usd')
            dot_index = -1
            i = rindex - 1
            while (i >= 0 and (text[i: rindex].isdigit() or text[i] == '.' or (dot_index != -1 and text[i:dot_index].isdigit()))):
                if text[i] == '.':
                    dot_index = i
                i -= 1
            return float(text[i + 1:rindex])
        case ('jpy'):
            for i in jpy:
                text = text.replace(i, 'jpy')
            rindex = text.find('jpy')
            dot_index = -1
            i = rindex - 1
            while (i >= 0 and (text[i: rindex].isdigit() or text[i] == '.' or (dot_index != -1 and text[i:dot_index].isdigit()))):
                if text[i] == '.':
                    dot_index = i
                i -= 1
            return float(text[i + 1:rindex])
        case ('hkd'):
            for i in hkd:
                text = text.replace(i, 'hkd')
            rindex = text.find('hkd')
            dot_index = -1
            i = rindex - 1
            while (i >= 0 and (text[i: rindex].isdigit() or text[i] == '.' or (dot_index != -1 and text[i:dot_index].isdigit()))):
                if text[i] == '.':
                    dot_index = i
                i -= 1
            return float(text[i + 1:rindex])
        case ('krw'):
            for i in krw:
                text = text.replace(i, 'krw')
            rindex = text.find('krw')
            dot_index = -1
            i = rindex - 1
            while (i >= 0 and (text[i: rindex].isdigit() or text[i] == '.' or (dot_index != -1 and text[i:dot_index].isdigit()))):
                if text[i] == '.':
                    dot_index = i
                i -= 1
            return float(text[i + 1:rindex])
        case ('cny'):
            for i in cny:
                text = text.replace(i, 'cny')
            rindex = text.find('cny')
            dot_index = -1
            i = rindex - 1
            while (i >= 0 and (text[i: rindex].isdigit() or text[i] == '.' or (dot_index != -1 and text[i:dot_index].isdigit()))):
                if text[i] == '.':
                    dot_index = i
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
                divs = tr.find_all('div')
                if len(divs) > 2 and '美金 (USD)' in divs[2].text:
                    return f"{price}美金(USD) = {price * float(tr.find_all('td')[2].text)} 新台幣(TWD)"    
        case ('jpy'):
            for tr in trs:
                divs = tr.find_all('div')
                if len(divs) > 2 and '日圓 (JPY)' in tr.find_all('div')[2].text:
                    return f"{price}日圓(JPY) = {price * float(tr.find_all('td')[2].text)} 新台幣(TWD)"
        case ('hkd'):
            for tr in trs:
                divs = tr.find_all('div')
                if len(divs) > 2 and '港幣 (HKD)' in tr.find_all('div')[2].text:
                    return f"{price}港幣(HKD) = {price * float(tr.find_all('td')[2].text)} 新台幣(TWD)"
        case ('krw'):
            for tr in trs:
                divs = tr.find_all('div')
                if len(divs) > 2 and '韓元 (KRW)' in tr.find_all('div')[2].text:
                    return f"{price}韓元(KRW) = {price * float(tr.find_all('td')[2].text)} 新台幣(TWD)"
        case ('cny'):
            for tr in trs:
                divs = tr.find_all('div')
                if len(divs) > 2 and '人民幣 (CNY)' in tr.find_all('div')[2].text:
                    return f"{price}人民幣(CNY) = {price * float(tr.find_all('td')[2].text)} 新台幣(TWD)"
from linebot import LineBotApi
from linebot.models import TextSendMessage
from LineBot.settings import LINE_CHANNEL_ACCESS_TOKEN
from BotTest.services.weather import get_today_weather, weather_template_message
from BotTest.services.ptt_beauty import get_beauty_imgs, beauty_template_message

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

def push_message(user_id, push_text_str):
    line_bot_api.push_message(user_id, TextSendMessage(text=push_text_str))

def push_morning_messages(user_id):
    imgs, texts, urls = get_beauty_imgs(10)
    line_bot_api.push_message(user_id, [
            TextSendMessage(text='早安'),
            weather_template_message(get_today_weather()),
            beauty_template_message(imgs, texts, urls)
        ]
    )
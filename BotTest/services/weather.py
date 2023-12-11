import requests as req
from linebot.models import TemplateSendMessage, CarouselTemplate, CarouselColumn, PostbackAction
from LineBot.settings import WEATHER_API_KEY


def get_today_weather():
    url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={WEATHER_API_KEY}'
    response = req.get(url)
    data = response.json()
    # weather['臺北市']={wx: ['', ''], pop: ['', ''], minT: ['', ''], maxT: ['', '']}
    # [0]6:00-18:00 [1]18:00-6:00 T氣溫X~X POP降雨機率 Wx天氣情況
    locations = data['records']['location']
    weather = {}
    times = locations[0]['weatherElement'][0]['time']
    weather['startTime'] = fetch_time_info(times, 'startTime')
    weather['endTime'] = fetch_time_info(times, 'endTime')
    for location in locations:
        match location['locationName']:
            case ('臺北市'):
                weather['臺北市'] = {}
                for we in location['weatherElement']:
                    match we['elementName']:
                        case ('Wx'):
                            weather['臺北市']['wx'] = fetch_weather_info(we)
                        case ('PoP'):
                            weather['臺北市']['pop'] = fetch_weather_info(we)
                        case ('MinT'):
                            weather['臺北市']['minT'] = fetch_weather_info(we)
                        case ('MaxT'):
                            weather['臺北市']['maxT'] = fetch_weather_info(we) 
            case ('新北市'):
                weather['新北市'] = {}
                for we in location['weatherElement']:
                    match we['elementName']:
                        case ('Wx'):
                            weather['新北市']['wx'] = fetch_weather_info(we)
                        case ('PoP'):
                            weather['新北市']['pop'] = fetch_weather_info(we)
                        case ('MinT'):
                            weather['新北市']['minT'] = fetch_weather_info(we)
                        case ('MaxT'):
                            weather['新北市']['maxT'] = fetch_weather_info(we) 
            
            case ('臺中市'):
                weather['臺中市'] = {}
                for we in location['weatherElement']:
                    match we['elementName']:
                        case ('Wx'):
                            weather['臺中市']['wx'] = fetch_weather_info(we)
                        case ('PoP'):
                            weather['臺中市']['pop'] = fetch_weather_info(we)
                        case ('MinT'):
                            weather['臺中市']['minT'] = fetch_weather_info(we)
                        case ('MaxT'):
                            weather['臺中市']['maxT'] = fetch_weather_info(we) 
            
            case ('彰化縣'):
                weather['彰化縣'] = {}
                for we in location['weatherElement']:
                    match we['elementName']:
                        case ('Wx'):
                            weather['彰化縣']['wx'] = fetch_weather_info(we)
                        case ('PoP'):
                            weather['彰化縣']['pop'] = fetch_weather_info(we)
                        case ('MinT'):
                            weather['彰化縣']['minT'] = fetch_weather_info(we)
                        case ('MaxT'):
                            weather['彰化縣']['maxT'] = fetch_weather_info(we) 
                
            case ('雲林縣'):
                weather['雲林縣'] = {}
                for we in location['weatherElement']:
                    match we['elementName']:
                        case ('Wx'):
                            weather['雲林縣']['wx'] = fetch_weather_info(we)
                        case ('PoP'):
                            weather['雲林縣']['pop'] = fetch_weather_info(we)
                        case ('MinT'):
                            weather['雲林縣']['minT'] = fetch_weather_info(we)
                        case ('MaxT'):
                            weather['雲林縣']['maxT'] = fetch_weather_info(we) 
                
            case ('臺南市'):
                weather['臺南市'] = {}
                for we in location['weatherElement']:
                    match we['elementName']:
                        case ('Wx'):
                            weather['臺南市']['wx'] = fetch_weather_info(we)
                        case ('PoP'):
                            weather['臺南市']['pop'] = fetch_weather_info(we)
                        case ('MinT'):
                            weather['臺南市']['minT'] = fetch_weather_info(we)
                        case ('MaxT'):
                            weather['臺南市']['maxT'] = fetch_weather_info(we) 
                
            case ('高雄市'):
                weather['高雄市'] = {}
                for we in location['weatherElement']:
                    match we['elementName']:
                        case ('Wx'):
                            weather['高雄市']['wx'] = fetch_weather_info(we)
                        case ('PoP'):
                            weather['高雄市']['pop'] = fetch_weather_info(we)
                        case ('MinT'):
                            weather['高雄市']['minT'] = fetch_weather_info(we)
                        case ('MaxT'):
                            weather['高雄市']['maxT'] = fetch_weather_info(we) 
            
            case ('宜蘭縣'):
                weather['宜蘭縣'] = {}
                for we in location['weatherElement']:
                    match we['elementName']:
                        case ('Wx'):
                            weather['宜蘭縣']['wx'] = fetch_weather_info(we)
                        case ('PoP'):
                            weather['宜蘭縣']['pop'] = fetch_weather_info(we)
                        case ('MinT'):
                            weather['宜蘭縣']['minT'] = fetch_weather_info(we)
                        case ('MaxT'):
                            weather['宜蘭縣']['maxT'] = fetch_weather_info(we) 
            
            case ('桃園市'):
                weather['桃園市'] = {}
                for we in location['weatherElement']:
                    match we['elementName']:
                        case ('Wx'):
                            weather['桃園市']['wx'] = fetch_weather_info(we)
                        case ('PoP'):
                            weather['桃園市']['pop'] = fetch_weather_info(we)
                        case ('MinT'):
                            weather['桃園市']['minT'] = fetch_weather_info(we)
                        case ('MaxT'):
                            weather['桃園市']['maxT'] = fetch_weather_info(we) 
                
            case ('苗栗縣'):
                weather['苗栗縣'] = {}
                for we in location['weatherElement']:
                    match we['elementName']:
                        case ('Wx'):
                            weather['苗栗縣']['wx'] = fetch_weather_info(we)
                        case ('PoP'):
                            weather['苗栗縣']['pop'] = fetch_weather_info(we)
                        case ('MinT'):
                            weather['苗栗縣']['minT'] = fetch_weather_info(we)
                        case ('MaxT'):
                            weather['苗栗縣']['maxT'] = fetch_weather_info(we)
    return weather

def fetch_weather_info(we):
    return [we['time'][0]['parameter']['parameterName'], we['time'][1]['parameter']['parameterName'], we['time'][2]['parameter']['parameterName']]

def fetch_time_info(times, key):
    times = [times[0][key], times[1][key], times[2][key]]
    for i in range(len(times)):
        date_strings = times[i].split('-') # 2022,10,20 18:00:00
        time_strings = date_strings[2].split(':') # 20 18,00,00
        times[i] = f"{date_strings[1]}/{time_strings[0]}:{time_strings[1]}"
    return times

def weather_template_message(weather):
    return TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    title='臺北市',
                    text=f"{weather['startTime'][0]} ~ {weather['endTime'][0]} /\n{weather['startTime'][1]} ~ {weather['endTime'][1]}",
                    actions=[
                        PostbackAction(
                            label=f"{weather['臺北市']['minT'][0]}°C~{weather['臺北市']['maxT'][0]}°C/{weather['臺北市']['minT'][1]}°C~{weather['臺北市']['maxT'][1]}°C",
                            data='test'
                        ),
                        PostbackAction(
                            label=f"{weather['臺北市']['pop'][0]}% / {weather['臺北市']['pop'][1]}%",
                            data='test'
                        ),
                        PostbackAction(
                            label=f"{weather['臺北市']['wx'][0]} / {weather['臺北市']['wx'][1]}"[:20],
                            data='test'
                        )
                    ]
                ),
                CarouselColumn(
                    title='新北市',
                    text=f"{weather['startTime'][0]} ~ {weather['endTime'][0]} /\n{weather['startTime'][1]} ~ {weather['endTime'][1]}",
                    actions=[
                        PostbackAction(
                            label=f"{weather['新北市']['minT'][0]}°C~{weather['新北市']['maxT'][0]}°C/{weather['新北市']['minT'][1]}°C~{weather['新北市']['maxT'][1]}°C",
                            data='test'
                        ),
                        PostbackAction(
                            label=f"{weather['新北市']['pop'][0]}% / {weather['新北市']['pop'][1]}%",
                            data='test'
                        ),
                        PostbackAction(
                            label=f"{weather['新北市']['wx'][0]} / {weather['新北市']['wx'][1]}"[:20],
                            data='test'
                        )
                    ]
                ),
                CarouselColumn(
                    title='臺中市',
                    text=f"{weather['startTime'][0]} ~ {weather['endTime'][0]} /\n{weather['startTime'][1]} ~ {weather['endTime'][1]}",
                    actions=[
                        PostbackAction(
                            label=f"{weather['臺中市']['minT'][0]}°C~{weather['臺中市']['maxT'][0]}°C/{weather['臺中市']['minT'][1]}°C~{weather['臺中市']['maxT'][1]}°C",
                            data='test'
                        ),
                        PostbackAction(
                            label=f"{weather['臺中市']['pop'][0]}% / {weather['臺中市']['pop'][1]}%",
                            data='test'
                        ),
                        PostbackAction(
                            label=f"{weather['臺中市']['wx'][0]} / {weather['臺中市']['wx'][1]}"[:20],
                            data='test'
                        )
                    ]
                ),
                CarouselColumn(
                    title='彰化縣',
                    text=f"{weather['startTime'][0]} ~ {weather['endTime'][0]} /\n{weather['startTime'][1]} ~ {weather['endTime'][1]}",
                    actions=[
                        PostbackAction(
                            label=f"{weather['彰化縣']['minT'][0]}°C~{weather['彰化縣']['maxT'][0]}°C/{weather['彰化縣']['minT'][1]}°C~{weather['彰化縣']['maxT'][1]}°C",
                            data='test'
                        ),
                        PostbackAction(
                            label=f"{weather['彰化縣']['pop'][0]}% / {weather['彰化縣']['pop'][1]}%",
                            data='test'
                        ),
                        PostbackAction(
                            label=f"{weather['彰化縣']['wx'][0]} / {weather['彰化縣']['wx'][1]}"[:20],
                            data='test'
                        )
                    ]
                ),
                CarouselColumn(
                    title='雲林縣',
                    text=f"{weather['startTime'][0]} ~ {weather['endTime'][0]} /\n{weather['startTime'][1]} ~ {weather['endTime'][1]}",
                    actions=[
                        PostbackAction(
                            label=f"{weather['雲林縣']['minT'][0]}°C~{weather['雲林縣']['maxT'][0]}°C/{weather['雲林縣']['minT'][1]}°C~{weather['雲林縣']['maxT'][1]}°C",
                            data='test'
                        ),
                        PostbackAction(
                            label=f"{weather['雲林縣']['pop'][0]}% / {weather['雲林縣']['pop'][1]}%",
                            data='test'
                        ),
                        PostbackAction(
                            label=f"{weather['雲林縣']['wx'][0]} / {weather['雲林縣']['wx'][1]}"[:20],
                            data='test'
                        )
                    ]
                ),
                CarouselColumn(
                    title='臺南市',
                    text=f"{weather['startTime'][0]} ~ {weather['endTime'][0]} /\n{weather['startTime'][1]} ~ {weather['endTime'][1]}",
                    actions=[
                        PostbackAction(
                            label=f"{weather['臺南市']['minT'][0]}°C~{weather['臺南市']['maxT'][0]}°C/{weather['臺南市']['minT'][1]}°C~{weather['臺南市']['maxT'][1]}°C",
                            data='test'
                        ),
                        PostbackAction(
                            label=f"{weather['臺南市']['pop'][0]}% / {weather['臺南市']['pop'][1]}%",
                            data='test'
                        ),
                        PostbackAction(
                            label=f"{weather['臺南市']['wx'][0]} / {weather['臺南市']['wx'][1]}"[:20],
                            data='test'
                        )
                    ]
                ),
                CarouselColumn(
                    title='高雄市',
                    text=f"{weather['startTime'][0]} ~ {weather['endTime'][0]} /\n{weather['startTime'][1]} ~ {weather['endTime'][1]}",
                    actions=[
                        PostbackAction(
                            label=f"{weather['高雄市']['minT'][0]}°C~{weather['高雄市']['maxT'][0]}°C/{weather['高雄市']['minT'][1]}°C~{weather['高雄市']['maxT'][1]}°C",
                            data='test'
                        ),
                        PostbackAction(
                            label=f"{weather['高雄市']['pop'][0]}% / {weather['高雄市']['pop'][1]}%",
                            data='test'
                        ),
                        PostbackAction(
                            label=f"{weather['高雄市']['wx'][0]} / {weather['高雄市']['wx'][1]}"[:20],
                            data='test'
                        )
                    ]
                ),
                CarouselColumn(
                    title='宜蘭縣',
                    text=f"{weather['startTime'][0]} ~ {weather['endTime'][0]} /\n{weather['startTime'][1]} ~ {weather['endTime'][1]}",
                    actions=[
                        PostbackAction(
                            label=f"{weather['宜蘭縣']['minT'][0]}°C~{weather['宜蘭縣']['maxT'][0]}°C/{weather['宜蘭縣']['minT'][1]}°C~{weather['宜蘭縣']['maxT'][1]}°C",
                            data='test'
                        ),
                        PostbackAction(
                            label=f"{weather['宜蘭縣']['pop'][0]}% / {weather['宜蘭縣']['pop'][1]}%",
                            data='test'
                        ),
                        PostbackAction(
                            label=f"{weather['宜蘭縣']['wx'][0]} / {weather['宜蘭縣']['wx'][1]}"[:20],
                            data='test'
                        )
                    ]
                ),
                CarouselColumn(
                    title='桃園市',
                    text=f"{weather['startTime'][0]} ~ {weather['endTime'][0]} /\n{weather['startTime'][1]} ~ {weather['endTime'][1]}",
                    actions=[
                        PostbackAction(
                            label=f"{weather['桃園市']['minT'][0]}°C~{weather['桃園市']['maxT'][0]}°C/{weather['桃園市']['minT'][1]}°C~{weather['桃園市']['maxT'][1]}°C",
                            data='test'
                        ),
                        PostbackAction(
                            label=f"{weather['桃園市']['pop'][0]}% / {weather['桃園市']['pop'][1]}%",
                            data='test'
                        ),
                        PostbackAction(
                            label=f"{weather['桃園市']['wx'][0]} / {weather['桃園市']['wx'][1]}"[:20],
                            data='test'
                        )
                    ]
                ),
                CarouselColumn(
                    title='苗栗縣',
                    text=f"{weather['startTime'][0]} ~ {weather['endTime'][0]} /\n{weather['startTime'][1]} ~ {weather['endTime'][1]}",
                    actions=[
                        PostbackAction(
                            label=f"{weather['苗栗縣']['minT'][0]}°C~{weather['苗栗縣']['maxT'][0]}°C/{weather['苗栗縣']['minT'][1]}°C~{weather['苗栗縣']['maxT'][1]}°C",
                            data='test'
                        ),
                        PostbackAction(
                            label=f"{weather['苗栗縣']['pop'][0]}% / {weather['苗栗縣']['pop'][1]}%",
                            data='test'
                        ),
                        PostbackAction(
                            label=f"{weather['苗栗縣']['wx'][0]} / {weather['苗栗縣']['wx'][1]}"[:20],
                            data='test'
                        )
                    ]
                )
            ]
        )
    )

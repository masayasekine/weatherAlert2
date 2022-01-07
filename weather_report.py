import requests
import json

def getWeatherReport():
    # 千葉県
    # TODO: エリアを個人別で登録できるようにしたい
    area_code = '120000'

    url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/{0}.json'.format(area_code)
    json = requests.get(url).json()

    report = ''
    areas = json[0]['timeSeries'][0]['areas']
    for area in areas:
        name = area['area']['name']
        weather = area['weathers'][1]
        report += name + ': ' + weather + '\n'

    return report



    # # JSONの構造上この位置に東京の3日分の予報が格納される
    # weathers = json[0]['timeSeries'][0]['areas'][0]['weathers']
    # # 当日の予報を取得
    # weather = weathers[0]
    # print(weather)
    # return weather
import requests
import json

def getWeatherReport(day):
    # 千葉県
    # TODO: エリアを個人別で登録できるようにしたい
    area_code = '120000'

    url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/{0}.json'.format(area_code)
    json = requests.get(url).json()

    report = ''
    areas = json[0]['timeSeries'][0]['areas']
    for area in areas:
        name = area['area']['name']
        weather = area['weathers'][day]
        report += name + ': ' + weather + '\n'

    return report

def getPopsReport():
    # 千葉県
    # TODO: エリアを個人別で登録できるようにしたい
    area_code = '120000'

    url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/{0}.json'.format(area_code)
    json = requests.get(url).json()

    report = '降水確率\n'
    # 降水確率
    pop_areas = json[0]['timeSeries'][1]['areas']

    for area in pop_areas:
        name = area['area']['name']
        report += name + '\n'
        for i, pop in enumerate(area['pops']):
            report += str((3 + (i * 6))) + ':00 -> ' + pop + '% \n'
    # 最低/最高気温
    tmp_areas = json[0]['timeSeries'][2]['areas']
    for area in tmp_areas:
        name = area['area']['name']
        report += name + '\n'
        tmps = area['temps']
        report += '最低気温: ' + tmps[0] + '℃, '
        report += '最高気温: ' + tmps[1] + '℃\n'
    return report

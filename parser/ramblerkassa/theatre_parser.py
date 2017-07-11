import json

import requests
from bs4 import BeautifulSoup


# tagid = {
#     'ballet': 60,
#     'child': 83,
#     'child performance': 534,
#     'dramatical': 79,
#     'dramatical performance': 81,
#     'classical drama': 1983,
#     'comedy': 63,
#     'muppet': 1130,
#     'mono performance': 1147,
#     'book musical': 80,
#     'musical performance': 1145,
#     'musical': 68,
#     'opera': 67,
#     'operetta': 1146,
#     'perfomance': 1136, # в значении перфоманс
#     'plastic': 1740,
#     'premiere': 78,
#     'modern': 1738,
#     'dancing perfomance': 1135,
#     'creative evening': 1142,
#     'circus': 2063,
#     'circus show': 597
# }


def fetch_content(url, params=None):
    try:
        result = requests.get(url, params=params)
        result.raise_for_status()
        return result.text
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print(e)


def fetch_json(skip):
    url = 'https://kassa.rambler.ru/creationsblock/9'
    params = {
                'currenttab': 'Theatres',
                'skip': skip
        }
    raw_data = fetch_content(url, params)
    if raw_data:
        return json.loads(raw_data)


def fetch_number_of_perfomances_and_urls(skip=0):
    raw_data = fetch_json(skip)
    perfomances_url = []
    html = raw_data['list']
    bs = BeautifulSoup(html, 'html.parser')
    for item in bs.find_all('a', itemprop='url'):
        perfomances_url.append(item.get('href'))
    number_of_perfomances = raw_data['nextbutton']['text']
    skip = 18
    return int(number_of_perfomances.split()[-1]), perfomances_url, skip


def fetch_perfomance_info(bs):
    production_info = bs.find('dl', class_='item_desc__peop')
    raw_actors = production_info.find('span', itemprop='name')
    raw_production = production_info.find('dd')
    raw_producer = production_info.find('dd', itemprop="attendee")
    raw_price = bs.find('b', class_="item_costs__cost")
    return {
        'title': bs.find('h1', itemprop='name').text,
        'production': raw_production.text if raw_production else None,
        'actors': raw_actors.text if raw_actors else None,
        'producer': raw_producer.text if raw_producer else None,
        'price': raw_price.text if raw_price else None
    }



def fetch_perfomance_date_and_theatre_info(bs):
    raw_data = bs.find('div', class_="rasp_names")
    if raw_data:
        theatre_name = raw_data.find('span', class_="s-name").text
        raw_theatre_url = raw_data.find('a')
        raw_data = raw_data.find('div', class_="rasp_name3 s-place")
        raw_theatre_adress = raw_data.find('span')
        raw_underground_station = raw_data.find('div', class_="rasp_place_metro")
        perfomances_date = []
        for raw in bs.find_all('div', class_='rasp_item'):
            perfomances_date.append(raw.find('div', class_="rasp_date").text)
        return {
            'theatre name': theatre_name,
            'theatre url': raw_theatre_url.get('href') if raw_theatre_url else None,
            'theatre adress': raw_theatre_adress.text if raw_theatre_adress else None,
            'underground station': raw_underground_station.text if raw_underground_station else None,
            'perfomance date': perfomances_date
        }


if __name__ == '__main__':
    number_of_perfomances, perfomances_url, skip = fetch_number_of_perfomances_and_urls()
    while skip < number_of_perfomances:
        perfomances_url += fetch_number_of_perfomances_and_urls(skip)[1]
        skip += 18
    for url in perfomances_url[:2]:        
        html = fetch_content(url)
        bs = BeautifulSoup(html,'html.parser')
        print(fetch_perfomance_info(bs))
        print(fetch_perfomance_date_and_theatre_info(bs))

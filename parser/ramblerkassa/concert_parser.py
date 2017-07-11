import json

import requests
from bs4 import BeautifulSoup


def fetch_content(url, params=None):
    try:
        result = requests.get(url, params=params)
        result.raise_for_status()
        return result.text
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print(e)


def fetch_json(skip):
    url = 'https://kassa.rambler.ru/creationsblock/4'
    params = {
                'currenttab': 'Concerts',
                'skip': skip
        }
    raw_data = fetch_content(url, params)
    if raw_data:
        return json.loads(raw_data)


def fetch_number_of_concerts_and_urls(skip=0):
    raw_data = fetch_json(skip)
    perfomances_url = []
    html = raw_data['list']
    bs = BeautifulSoup(html, 'html.parser')
    for item in bs.find_all('a', itemprop='url'):
        perfomances_url.append(item.get('href'))
    number_of_perfomances = raw_data['nextbutton']['text']
    skip = 24
    return int(number_of_perfomances.split()[-1]), perfomances_url, skip


def fetch_concert_info(bs):
    raw_data = bs.find('div', class_='item_datas')
    raw_description = raw_data.find('div', itemprop="description")
    raw_price = bs.find('b', class_="item_costs__cost")
    return {
        'title': bs.find('h1', itemprop='name').text,
        'description': raw_description.text.strip() if raw_description else None,
        'price': raw_price.text if raw_price else None
    }


def fetch_concert_date_and_place_info(bs):
    raw_data = bs.find('div', class_="rasp_names")
    if raw_data:
        raw_place_name = raw_data.find('span', class_="s-name")
        raw_place_url = raw_data.find('a')
        raw_data = raw_data.find('div', class_="rasp_name3 s-place")
        raw_place_adress = raw_data.find('span')
        raw_underground_station = raw_data.find('div', class_="rasp_place_metro")
        concert_date = []
        for raw in bs.find_all('div', class_='rasp_item'):
            concert_date.append(raw.find('div', class_="rasp_date").text)
        return {
            'place name': raw_place_name.text if raw_place_name else None,
            'place url': raw_place_url.get('href') if raw_place_url else None,
            'place adress': raw_place_adress.text if raw_place_adress else None,
            'underground station': raw_underground_station.text if raw_underground_station else None,
            'perfomance date': concert_date
        }


if __name__ == '__main__':
    number_of_concerts, concerts_url, skip = fetch_number_of_concerts_and_urls()
    while skip < number_of_concerts:
        concerts_url += fetch_number_of_concerts_and_urls(skip)[1]
        skip += 24
    for url in concerts_url[:2]:
        print(url)
        html = fetch_content(url)
        bs = BeautifulSoup(html,'html.parser')
        print(fetch_concert_info(bs))
        print(fetch_concert_date_and_place_info(bs))

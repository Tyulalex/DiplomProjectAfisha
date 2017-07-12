import json

import requests
from bs4 import BeautifulSoup


def get_url_params(event):
    event_city = {
        'films': 17,
        'concerts': 4,
        'theatres': 9
    }
    currenttab = {
        'films': 'Cinemas',
        'concerts': 'Concerts',
        'theatres': 'Theatres'
    }
    return event_city.get(event), currenttab.get(event)


def fetch_content(url, params=None):
    try:
        result = requests.get(url, params=params)
        result.raise_for_status()
        return result.text
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print(e)


def fetch_json(skip, event):
    url = 'https://kassa.rambler.ru/creationsblock/%s' %get_url_params(event)[0]
    params = {
                'currenttab': get_url_params(event)[1],
                'skip': skip
        }
    raw_data = fetch_content(url, params)
    if raw_data:
        return json.loads(raw_data)


def fetch_number_of_events_and_urls(skip, event):
    raw_data = fetch_json(skip, event)
    events_url = []
    html = raw_data['list']
    bs = BeautifulSoup(html, 'html.parser')
    if event == 'theatres':
        skip = 18
    else:
        skip = 24
    for item in bs.find_all('a', class_="mb_item "):
        events_url.append(item.get('href'))
    number_of_events = raw_data['nextbutton']['text']
    return int(number_of_events.split()[-1]), events_url, skip


#only for concerts and theatres-------------------------------------------------


def fetch_events_date_and_place_info(bs):
    raw_data = bs.find('div', class_="rasp_names")
    if raw_data:
        place = raw_data.find('span', class_="s-name").text
        raw_place_url = raw_data.find('a')
        raw_data = raw_data.find('div', class_="rasp_name3 s-place")
        raw_place_adress = raw_data.find('span')
        raw_underground_station = raw_data.find('div', class_="rasp_place_metro")
        event_date = []
        for raw in bs.find_all('div', class_='rasp_item'):
            event_date.append(raw.find('div', class_="rasp_date").text)
        return {
            'place': place,
            'place url': raw_place_url.get('href') if raw_place_url else None,
            'place adress': raw_place_adress.text if raw_place_adress else None,
            'underground station': raw_underground_station.text if raw_underground_station else None,
            'event date': event_date
        }

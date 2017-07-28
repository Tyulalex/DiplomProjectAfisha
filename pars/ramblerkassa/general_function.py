import json

import requests
from bs4 import BeautifulSoup

import special_function


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


def get_events_url_file(event):
    number_of_events, events_url, skip = fetch_number_of_events_and_urls(0, event)
    while skip < number_of_events:
        events_url += fetch_number_of_events_and_urls(skip, event)[1]
        if event == 'theatres':
            skip += 18
        else:
            skip +=24
    with open('%s.txt' %event, 'w') as f:
        for url in events_url:
            f.write(url + '\n')


def get_events_info(event):
    with open('%s.txt' %event, 'r') as f:
        for line in f:
            url = f.readline().strip()
            if url:
                html = fetch_content(url)
                bs = BeautifulSoup(fetch_content(url),'html.parser')
                if event == 'films':
                    return  special_function.fetch_film_info(bs), \
                            special_function.fetch_cinema_info(bs)
                elif event == 'theatres':
                    return special_function.fetch_perfomance_info(bs),\
                           special_function.fetch_events_date_and_place_info(bs)
                else:
                    return special_function.fetch_concert_info(bs),\
                           special_function.fetch_events_date_and_place_info(bs)

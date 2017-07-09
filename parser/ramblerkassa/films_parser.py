import requests, copy, json
from bs4 import BeautifulSoup

from fetch_film_info import *


def fetch_content(url, params=None):
    try:
        result = requests.get(url, params=params)
        result.raise_for_status()
        return result.text
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print(e)


def fetch_json(next_elements):
    url = 'https://kassa.rambler.ru/creationsblock/17'
    params = {
                'currenttab': 'Cinemas',
                'skip': next_elements
        }
    raw_data = fetch_content(url, params)
    if raw_data:
        return json.loads(raw_data)


def fetch_number_of_films_and_urls(next_elements=0):
    raw_data = fetch_json(next_elements)
    films_url = []
    html = raw_data['list']
    bs = BeautifulSoup(html, 'html.parser')
    for item in bs.find_all('span', itemprop='url'):
        films_url.append(item.find('a').get('href'))
    number_of_films = raw_data['nextbutton']['text']
    next_elements = 24
    return int(number_of_films.split()[-1]), films_url, next_elements


def fetch_film_info(bs):
    return {
        'title ru': receive_film_name(bs, 'ru'),
        'title en': receive_film_name(bs, 'en'),
        'genre': receive_film_genre(bs),
        'age limit': receive_film_age_limit(bs),
        'film description': receive_film_desription(bs),
        'film len': receive_film_len_countrymaker_producer(bs)[0],
        'film countrymaker': receive_film_len_countrymaker_producer(bs)[1],
        'film producer': receive_film_len_countrymaker_producer(bs)[2],
        'film actors': receive_film_actors(bs)
    }


def get_showtimes_and_price(showtime_html):
    showtimes_info_list = []
    for showtime in showtime_html.find_all('li', itemtype="http://schema.org/AggregateOffer"):
        min_price = showtime.find('meta', itemprop="lowPrice")
        max_price = showtime.find('meta', itemprop="highPrice")
        showtimes_info_list.append({
            'showtime': showtime.text.strip(),
            'min price': min_price.get('content') if min_price else None,
            'max price': max_price.get('content') if max_price else None
        })
    return showtimes_info_list


def fetch_cinema_info(bs):
    cinema_info_list = []
    for item in bs.find_all('div', class_="rasp_item_in"):
        cinema_info = {}
        cinema_info['name'] = item.find('span', itemprop="name").text
        cinema_info['link'] = item.find('a', itemprop='url').get('href')
        cinema_info['adress'] = item.find('span', itemprop="streetAddress").text
        if item.find('div', class_="rasp_place_metro"):
            cinema_info['underground station'] = item.find('div', class_="rasp_place_metro").text
        showtime_2D_html = item.find('ul', attrs={'data-format': 0})
        if showtime_2D_html:
            showtimes_info_2D_list = get_showtimes_and_price(showtime_2D_html)
        showtime_3D_html = item.find('ul', attrs={'data-format': 1})
        if showtime_3D_html:
            showtimes_info_3D_list = get_showtimes_and_price(showtime_3D_html)
        cinema_info['sessions_info_2D'] = showtimes_info_2D_list
        cinema_info['sessions_info_3D'] = showtimes_info_3D_list
        cinema_info_list.append(cinema_info)
    return cinema_info_list


if __name__ == '__main__':
    number_of_films, films_url, next_elements = fetch_number_of_films_and_urls()
    while next_elements < number_of_films:
        films_url += fetch_number_of_films_and_urls(next_elements)[1]
        next_elements += 24
    for url in films_url[:1]:
        html = fetch_content(url, params=False)
        bs = BeautifulSoup(html,'html.parser')
        print(fetch_film_info(bs))
        print(fetch_cinema_info(bs))

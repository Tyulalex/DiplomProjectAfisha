import requests, copy, json
from bs4 import BeautifulSoup

def get_html_json(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.json()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print(e)
        return False


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print(e)
        return False


def get_api_dict(url, dict_1=None, dict_2=None):
    html = get_html_json(url)
    if dict_2:
        return html[dict_1][dict_2]
    else:
        return html[dict_1]


def get_film_url(html, filter_1, filter_2, filter_3, quest):
    film_url = []
    bs = BeautifulSoup(html, 'html.parser')
    for item in bs.find_all(filter_1, itemprop=filter_2):
        film_url.append(item.find(filter_3).get(quest))
    return film_url


def get_film_data(url):
    film_data = []
    html = get_html(url)
    bs = BeautifulSoup(html, 'html.parser')
    film_name_ru = bs.find('h1', itemprop="name")
    film_name_en = bs.find('h2', class_='item_title2')
    film_descr = bs.find('span', class_="item_desc__text item_desc__text-full")
    film_data.append(film_name_ru.text)
    film_data.append(film_name_en.text.strip())
    film_data.append(film_descr.text)
    return(film_data)



if __name__ == "__main__":
    elements = 0
    count = 0
    film_url = []
    url = ('https://kassa.rambler.ru/creationsblock/17?currenttab=Cinemas&skip=%r' %elements)
    text = get_api_dict(url,'nextbutton', 'text')
    all_elements = int(text.split()[-1])
    while elements < all_elements:
        url = ('https://kassa.rambler.ru/creationsblock/17?currenttab=Cinemas&skip=%r' %elements)
        html = get_api_dict(url, 'list')
        film_url.append(get_film_url(html,'span', 'url', 'a', 'href'))
        elements += 24
    print(get_film_data('https://kassa.rambler.ru/msk/movie/78671'))

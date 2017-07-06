import requests, copy, json
from bs4 import BeautifulSoup


def fetch_content(url, params, next_elements=0):
    try:
        if params == False:
            result = requests.get(url)
            result.raise_for_status()
            return result.text
        else:
            result = requests.get(url, params=params)
            result.raise_for_status()
            return result.text
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print(e)
        return False


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
    if next_elements == 0:
        number_of_films = raw_data['nextbutton']['text']
        next_elements = 24
        return int(number_of_films .split()[-1]), films_url, next_elements
    else:
        return films_url

def get_beautifulsoup(url):
    html = fetch_content(url, params=False)
    return BeautifulSoup(html,'html.parser')


def fetch_film_info(bs):
    page_movie = bs.find('div',class_="width page_movie" )
    film_name_ru = bs.find('h1', itemprop="name")
    film_name_en = bs.find('h2', class_='item_title2')
    film_desciption = bs.find('span', class_="item_desc__text item_desc__text-full")
    if film_desciption == None:
        film_desciption =  bs.find('span', class_="item_desc__text")
    return  film_name_ru.text, film_name_en.text.strip(), film_desciption.text.strip()


def get_session_time_and_price(session_html):
    for session in session_html.find_all('li', itemtype="http://schema.org/AggregateOffer"):
        sessions_info = {}
        sessions_info['session_time_2D'] = session.text
        sessions_info['min price'] = session.find('meta', itemprop="lowPrice").get('content')
        sessions_info['max price'] = session.find('meta', itemprop="highPrice").get('content')
        sessions_info_list.append(sessions_info_2D)
    return sessions_info


def fetch_cinema_info(bs):
    cinema_info_list = []
    for item in bs.find_all('div', class_="rasp_item_in"):
        cinema_info = {}
        sessions_info_2D_list = []
        sessions_info_3D_list = []
        cinema_info['name'] = item.find('span', itemprop="name").text
        cinema_info['link'] = item.find('a', itemprop='url').get('href')
        cinema_info['adress'] = item.find('span', itemprop="streetAddress").text
        if item.find('div', class_="rasp_place_metro"):
            cinema_info['underground station'] = item.find('div', class_="rasp_place_metro").text
        # session_2D = item.find('ul', data-format="0")
        # sessions_info_2D = get_session_time_and_price(session_2D)
        # session_3D = item.find('ul', data-format="1")
        # if session_3D:
        #     sessions_info_3D = get_session_time_and_price(session_3D)
        # cinema_info['sessions_info_2D'] = sessions_info_2D_list
        # cinema_info['sessions_info_3D'] = sessions_info_3D_list
        cinema_info_list.append(cinema_info)
    return cinema_info_list


if __name__ == '__main__':
    number_of_films, films_url, next_elements = fetch_number_of_films_and_urls()
    while next_elements < number_of_films:
        films_url += fetch_number_of_films_and_url(next_elements)
        next_elements += 24
    for url in films_url[:1]:
        bs = get_beautifulsoup(url)
        print(fetch_film_info(bs))
        print(fetch_cinema_info(bs))

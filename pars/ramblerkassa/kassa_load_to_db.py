import json

import requests
from bs4 import BeautifulSoup

import general_function as gen_func
import special_function as spec_func


if __name__ == '__main__':
    #получаем файлы с url
    gen_func.get_events_url_file(concerts) # файл - concerts.txt
    gen_func.get_events_url_file(films)    # файл - films.txt
    gen_func.get_events_url_file(theatres) # файл - theatres.txt

    #получаем информацию с сайта
    'films'
    #информация по фильмам парсится на текущий день!
    with open('%s.txt' %films, 'r') as f:
        for line in f:
            url = f.readline().strip()
            if url:
                bs = (gen_func.fetch_content(url),'html.parser')
                films_dict = spec_func.fetch_film_info(bs)
                #films_dict будет содержать следующие ключи:
                # 'title ru' - название на русском, - общее поле
                # 'title en' - название на английском,
                # 'genre' - жанр фильма,
                # 'age limit' - возрастное ограничение,
                # 'film description', - общее поле
                # 'film len' - длина фильма,
                # 'film countrymaker' - страна - изготовитель фильма,
                # 'film producer' - режиссёр фильма,
                # 'film actors'
                cinemas_dict = spec_func.fetch_cinema_info(bs)
                #fcinemas_dict будет содержать список словарей, каждый будет иметь следующие ключи:
                # 'name' - название кинотеатра
                # 'link' - ссылка на кинотеатр
                # 'adress' - адрес кинотеатра
                # 'underground station' - станция метро, если такая имеется
                # 'sessions_info_2D' - информация по сеансам в 2D: минимальная и максимальная цена, время сеансов
                # 'sessions_info_3D' - информация по сеансам в 3D: минимальная и максимальная цена, время сеансов
    'concerts'
    with open('%s.txt' %concerts, 'r') as f:
        for line in f:
            url = f.readline().strip()
            if url:
                bs = (gen_func.fetch_content(url),'html.parser')
                concert_dict = spec_func.fetch_concert_info(bs)
                #concert_dict будет содержать следующие ключи:
                # 'title' - название, - общее поле
                # 'description' - описание, - общее поле с films
                # 'price' - цена - общее поле с theatres
                place_and_date_dict = spec_func.fetch_events_date_and_place_info(bs)
                # place_and_date_dict будет содержать следующие ключи:
                # 'place' - название места, - общее поле
                # 'place url' - ссылка на место, - общее поле (тоже что и link)
                # 'place adress' - адрес места, - общее поле
                # 'underground station' - станция метро, - общее поле
                # 'event date' - общее поле с theatres
    'theatres'
    with open('%s.txt' %theatres, 'r') as f:
        for line in f:
            url = f.readline().strip()
            if url:
                bs = (gen_func.fetch_content(url),'html.parser')
                perfomace_dict = spec_func.fetch_perfomance_info(bs)
                # perfomace_dict будет содержать следующие ключи:
                # 'title' - название спектакля, - общее поле
                # 'production' - постановка, общее поле с films
                # 'actors' - актёры, - общее поле с films
                # 'producer' - режжисёр , - общее поле с films
                # 'price' - цена
                place_and_date_dict = spec_func.fetch_events_date_and_place_info(bs)
                # place_and_date_dict будет содержать следующие ключи:
                # 'place' - название места, - общее поле
                # 'place url' - ссылка на место, - общее поле (тоже что и link)
                # 'place adress' - адрес места, - общее поле
                # 'underground station' - станция метро, - общее поле
                # 'event date' - общее поле с concerts

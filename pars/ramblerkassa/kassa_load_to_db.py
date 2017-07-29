import json

import requests
from bs4 import BeautifulSoup

import general_function as gen_func
import special_function as spec_func


if __name__ == '__main__':
    #получаем файлы с url
    gen_func.get_events_url_file('concerts') # файл - concerts.txt
    gen_func.get_events_url_file('films')    # файл - films.txt
    gen_func.get_events_url_file('theatres') # файл - theatres.txt
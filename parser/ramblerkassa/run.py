import json

import requests
from bs4 import BeautifulSoup

from general_function import *
from special_function import *


if __name__ == '__main__':
    number_of_events, events_url, skip = fetch_number_of_events_and_urls(0,'theatres')
    while skip < number_of_events:
        events_url += fetch_number_of_events_and_urls(skip, 'theatres')[1]
        skip += 18
    for url in events_url[:1]:
        html = fetch_content(url)
        bs = BeautifulSoup(html,'html.parser')
        print(fetch_perfomance_info(bs))
        print(fetch_events_date_and_place_info(bs))

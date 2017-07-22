import json

import requests
from bs4 import BeautifulSoup

import general_function



if __name__ == '__main__':
    print(general_function.get_events_info('films'))
    print(general_function.get_events_info('theatres'))
    print(general_function.get_events_info('concerts'))

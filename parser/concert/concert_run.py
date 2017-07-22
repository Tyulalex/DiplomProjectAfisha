import requests
from bs4 import BeautifulSoup


import concert_main_functions as main_func


if __name__ == '__main__':
    concerts_info_list = main_func.fetch_all_events_info(1)
    theatres_info_list = main_func.fetch_all_events_info(2)

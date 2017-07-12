#for films ---------------------------------------------------------------------


def receive_film_name(bs, languge):
    if languge == 'ru':
        return bs.find('h1', itemprop="name").text
    else:
        return bs.find('h2', class_='item_title2').text


def receive_film_genre(bs):
    return bs.find('h3', class_="item_title3").text.split()[:-1]


def receive_film_age_limit(bs):
    return bs.find('h3', class_="item_title3").text.split()[-1]


def receive_film_desription(bs):
    film_desciption_class = "item_desc__text item_desc__text-full"
    if bs.find('span', class_=film_desciption_class):
        description_class = film_desciption_class
    else:
        description_class = "item_desc__text"
    return bs.find('span', class_=description_class).text


def receive_film_len_countrymaker_producer(bs):
    film_info = []
    for item in bs.find_all('span', class_="dd"):
        film_info.append(item.text)
    return film_info[0], film_info[1], film_info[2]


def receive_film_actors(bs):
    actors_class = "item_peop__actors item_desc__text"
    actors_full_class = "item_peop__actors item_desc__text item_desc__text-full"
    if bs.find('span', class_=actors_class) != None:
        if bs.find('span', class_=actors_full_class):
            film_actors_class=actors_full_class
        else:
            film_actors_class = actors_class
        return  bs.find('span', film_actors_class).text


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


#for perfomances----------------------------------------------------------------


def fetch_perfomance_info(bs):
    production_info = bs.find('dl', class_='item_desc__peop')
    raw_actors = production_info.find('span', itemprop='name')
    raw_production = production_info.find('dd')
    raw_producer = production_info.find('dd', itemprop="attendee")
    raw_price = bs.find('b', class_="item_costs__cost")
    return {
        'title': bs.find('h1', itemprop='name').text,
        'production': raw_production.text if raw_production else None,
        'actors': raw_actors.text if raw_actors else None,
        'producer': raw_producer.text if raw_producer else None,
        'price': raw_price.text if raw_price else None
    }


#for concerts-------------------------------------------------------------------


def fetch_concert_info(bs):
    raw_data = bs.find('div', class_='item_datas')
    raw_description = raw_data.find('div', itemprop="description")
    raw_price = bs.find('b', class_="item_costs__cost")
    return {
        'title': bs.find('h1', itemprop='name').text,
        'description': raw_description.text.strip() if raw_description else None,
        'price': raw_price.text if raw_price else None
    }

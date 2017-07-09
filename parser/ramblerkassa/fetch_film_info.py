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

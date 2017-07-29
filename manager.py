# -*- coding: utf-8 -*-
import json
from geopy.distance import great_circle
from datetime import datetime

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from bs4 import BeautifulSoup

from app.server import create_app, db
from app.server.database_models import Place, PlaceType, ShowEvent, Event, EventCategory, AgeCategory, MetroStations
from lib.geo_parser import get_mos_metro_geo_data, get_coordinates_by_address
import pars.concert.concert_main_functions as main_func
import pars.ramblerkassa.general_function as gen_func
import pars.ramblerkassa.special_function as spec_func


app = create_app('default')
manager = Manager(app)
manager.add_command('db', MigrateCommand)
migrate = Migrate(app, db)


@manager.command
def fill_db():
    seed_catalogue()
    seed()
    seed_metro_stations()
    seed_stations_id()


@manager.command
def seed_catalogue():
    event_categories = ['Фильм', 'Спектакль', 'Концерт']
    age_categories = ['0+', '6+', '12+', '16+', '18+']
    place_types = ['Кинотеатры', 'Театры', 'Концертные площадки']

    for event_category in event_categories:
        db.session.add(EventCategory(category=event_category))
    for age_category in age_categories:
        db.session.add(AgeCategory(category=age_category))
    for place_type in place_types:
        db.session.add(PlaceType(type=place_type))
    db.session.commit()


@manager.command
def seed_metro_stations():
    metro_data_to_insert = get_mos_metro_geo_data()
    for metro_name, coordinates in metro_data_to_insert.items():
        db.session.add(MetroStations(name=metro_name, latitude=coordinates[0], longitude=coordinates[1]))
    db.session.commit()


@manager.command
def seed_stations_id():
    places = db.session.query(Place).all()
    for place in places:
        list_of_distance_to_metro_id_maps = []
        longitude, latitude = get_coordinates_by_address(address=place.address)
        metro_stations = db.session.query(MetroStations).all()
        for metro_station in metro_stations:
            distance = great_circle((float(longitude), float(latitude)), (metro_station.longitude, metro_station.latitude)).km
            list_of_distance_to_metro_id_maps.append((distance, metro_station.id))
        nearest_station_id = min(list_of_distance_to_metro_id_maps)[1]
        place.station_id = nearest_station_id
    db.session.commit()


@manager.command
def seed():
    "Add seed data to the database."
    with open('pars/ramblerkassa/films.txt', 'r') as f:
        for line in f:
            url = f.readline().strip()
            if url:
                bs = BeautifulSoup(main_func.fetch_content(url),'html.parser')
                films_dict = spec_func.fetch_film_info(bs)
                cinemas_dict = spec_func.fetch_cinema_info(bs)
                place_type_id = db.session.query(PlaceType). \
                filter(PlaceType.type == "Кинотеатры").one().id
                event = Event(
                    name=films_dict["title ru"], description="{0}{1}{2}".format(\
                    films_dict["film description"],\
                    films_dict["film len"], \
                    films_dict["film countrymaker"])
                )
                event.age_category_id = db.session.query(AgeCategory).filter(
                AgeCategory.category == films_dict["age limit"]).one().id

                event.event_category_id = db.session.query(EventCategory).filter(
                EventCategory.category == "Фильм").one().id
                db.session.add(event)
                db.session.commit()
                for cinema in cinemas_dict:



                    query_for_place = db.session.query(Place.id).filter(
                    (Place.name == cinema["name"])\
                     & (Place.address == cinema['adress'])
                    )
                    is_place_already_exists = db.session.query(query_for_place.exists()).scalar()
                    # if is_place_already_exists:
                    #     show_event.place_id = query_for_place.one().id
                    # else:
                    #     show_event.place = Place(
                    #         name=cinema["name"],\
                    #         address=cinema['adress'],\
                    #         place_type_id=place_type_id
                    #     )
                    # db.session.add(Place)
                    # db.session.commit()
                    if not is_place_already_exists:
                        db.session.add(Place(
                                name=cinema["name"],\
                                address=cinema['adress'],\
                                place_type_id=place_type_id
                            )
                        )
                        db.session.commit()
                    place_id = query_for_place.one().id


                    showtimes = cinema.get('sessions_info_2D')
                    if showtimes:
                        for showtime in showtimes:
                            date_now = datetime.now()
                            time_show = showtime['showtime'].split(':')
                            show_event = ShowEvent(
                            date_start=datetime(date_now.year,
                                                date_now.month,
                                                date_now.day,
                                                int(time_show[0]),
                                                int(time_show[1])
                                                ),
                            price_from=showtime['min price'],
                            price_to=showtime['max price'],
                            currency='RUB',
                            event_id=event.id,
                            place_id=place_id,
                            )
                            db.session.add(show_event)
                            db.session.commit()


if __name__ == '__main__':
    manager.run()

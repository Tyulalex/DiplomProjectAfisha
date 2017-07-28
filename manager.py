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
    concerts_info_list = fetch_all_events_info('pars/concert/concert_urls.txt')
    for seed_element in concerts_info_list:
        # place_type_id = db.session.query(PlaceType). \
        #     filter(PlaceType.type == seed_element["place_type"]).one().id

        date_start = seed_element["event date"]
        date_end = seed_element["event date"]

        event = Event(
            name=seed_element["event title"],
            description=seed_element["description"]
        )

        event.age_category_id = db.session.query(AgeCategory).filter(
            AgeCategory.category == seed_element["age limit"]).one().id

        # event.event_category_id = db.session.query(EventCategory).filter(
        #     EventCategory.category == seed_element["category"]).one().id

        show_event.event = event
        query_for_place = db.session.query(Place.id).filter(
            (Place.name == seed_element["place"]) & (Place.address == seed_element["address"])
        )
        is_place_already_exists = db.session.query(query_for_place.exists()).scalar()

        if is_place_already_exists:
            show_event.place_id = query_for_place.one().id
        else:
            show_event.place = Place(
                name=seed_element["place title"],
                address=seed_element["address"],
                place_type_id=place_type_id
            )

        db.session.add(show_event)
    db.session.commit()

if __name__ == '__main__':
    manager.run()

# -*- coding: utf-8 -*-
import json
from geopy.distance import great_circle
from datetime import datetime

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

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
    event_categories = ['Фильм', 'Спектакль', 'Выставка', 'Концерт']
    age_categories = ['0+', '6+', '12+', '16+', '18+']
    place_types = ['Кинотеатры', 'Театры', 'Выставочные площадки', 'Концертные площадки']

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

    with open('seed_db_test_data.json', encoding='utf-8') as data_file:
        seed_data = json.load(data_file)

    for seed_element in seed_data:
        place_type_id = db.session.query(PlaceType). \
            filter(PlaceType.type == seed_element["place_type"]).one().id

        date_start = datetime.strptime(seed_element["date_start"], '%d/%m/%Y %H:%M:%S')
        date_end = datetime.strptime(seed_element["date_end"], '%d/%m/%Y %H:%M:%S')

        show_event = ShowEvent(
            date_start=date_start, date_end=date_end, price_from=seed_element["price_from"],
            price_to=seed_element["price_to"], currency='RUB'
        )
        event = Event(
            name=seed_element["name"], description=seed_element["description"], rating=seed_element["rating"]
        )

        event.age_category_id = db.session.query(AgeCategory).filter(
            AgeCategory.category == seed_element["age_category"]).one().id

        event.event_category_id = db.session.query(EventCategory).filter(
            EventCategory.category == seed_element["category"]).one().id

        show_event.event = event
        query_for_place = db.session.query(Place.id).filter(
            (Place.name == seed_element["place_name"]) & (Place.address == seed_element["place_address"])
        )
        is_place_already_exists = db.session.query(query_for_place.exists()).scalar()

        if is_place_already_exists:
            show_event.place_id = query_for_place.one().id
        else:
            show_event.place = Place(
                name=seed_element["place_name"], address=seed_element["place_address"], place_type_id=place_type_id
            )

        db.session.add(show_event)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
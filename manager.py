# -*- coding: utf-8 -*-
import json
from datetime import datetime

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from bs4 import BeautifulSoup

from app.server import create_app, db
from app.server.database_models import Place, PlaceType, ShowEvent, Event, EventCategory, AgeCategory
from pars.concert.concert_main_functions import fetch_all_events_info


app = create_app('default')
manager = Manager(app)
manager.add_command('db', MigrateCommand)
migrate = Migrate(app, db)


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

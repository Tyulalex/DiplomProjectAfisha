# -*- coding: utf-8 -*-
import json
from datetime import datetime

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.server import create_app, db
from app.server.database_models import Place, PlaceType, ShowEvent, Event, EventCategory, AgeCategory

app = create_app('default')
manager = Manager(app)
manager.add_command('db', MigrateCommand)
migrate = Migrate(app, db)


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
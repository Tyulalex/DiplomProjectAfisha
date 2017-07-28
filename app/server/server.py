import json
from flask import Flask, render_template, request
from . import db
from . import create_app
from app.server.database_models import ShowEvent, Event, EventCategory, Place, MetroStations
from lib.dates_utils import get_this_month_date_range, get_this_year_date_range, get_this_week_date_range, \
    get_tomorrow_date_range, get_today_date_range

app = create_app(config_name='default')


@app.route('/')
def main_page():
    city = request.args.get('city')
    category = request.args.get('category')
    return render_template("base.html", data=[''])


def get_filtered_data_by_category(raw_events, category):
    return [event for event in raw_events if event.get('category', '').lower() == category]


def get_filtered_data_by_city(raw_events, city):
    return [event for event in raw_events if event.get('city', '').lower() == city.lower()]


@app.route('/concerts/')
def concerts():
    dates = request.args.get('dates')
    station = request.args.get('station')
    raw_concerts_events = db.session.query(ShowEvent).join(Event).join(EventCategory).\
        join(Place).join(MetroStations).filter(EventCategory.category == "Концерт").all()
    concert_events = raw_concerts_events
    if station:
        concert_events = [concert_event for concert_event in concert_events if concert_event.place.metro_station.name == station]
    if dates:
        arg_to_date_map = {
            'today': get_today_date_range(),
            'tomorrow': get_tomorrow_date_range(),
            'this_week': get_this_week_date_range(),
            'this_month': get_this_month_date_range(),
            'this_year': get_this_year_date_range()
        }

        date = arg_to_date_map[dates]

        concert_events = [concert_event for concert_event in concert_events
                if date[0] <= concert_event.date_start <= date[1]]

    metro_stations_list = db.session.query(MetroStations).all()
    places_list = db.session.query(Place).all()
    distinct_event_list = list(set([concert.event.name for concert in concert_events]))
    metro_data_source_json = json.dumps([metro.name for metro in metro_stations_list])
    place_data_source_json = json.dumps([place.name for place in places_list])
    event_list_to_json = json.dumps(distinct_event_list)
    return render_template("concerts.html", concert_events=concert_events, metro_stations_list=metro_stations_list,
                           metro_data_source_json=metro_data_source_json, place_data_source_json=place_data_source_json,
                           event_list_to_json=event_list_to_json)


@app.route('/concert/<path:eventId>')
def concert(eventId):
    concert_info = db.session.query(Event).filter(Event.id == eventId).one()
    concert_schedule = db.session.query(ShowEvent).join(Event).join(EventCategory). \
        join(Place).join(MetroStations).filter(Event.id == eventId).all()
    return render_template("concert.html", concert_info=concert_info, concert_schedule=concert_schedule)



























@app.route('/movies')
def cinema():
    pass
    #return render_template("index.html", data=get_filtered_data_by_category(raw_events, 'movies'))


@app.route('/theatres')
def theatres():
    pass
    #return render_template("index.html", data=get_filtered_data_by_category(raw_events, 'theatres'))


@app.route('/exhibition')
def exhibition():
    pass
    #return render_template("index.html", data=get_filtered_data_by_category(raw_events, 'exhibition'))

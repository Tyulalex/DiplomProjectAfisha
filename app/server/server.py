# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from . import db
from . import create_app
from app.server.database_models import ShowEvent, Event, EventCategory, Place, MetroStations

app = create_app(config_name='default')


@app.route('/')
def main_page():
    city = request.args.get('city')
    category = request.args.get('category')
    return render_template("index.html", data=[''])


def get_filtered_data_by_category(raw_events, category):
    return [event for event in raw_events if event.get('category', '').lower() == category]


def get_filtered_data_by_city(raw_events, city):
    return [event for event in raw_events if event.get('city', '').lower() == city.lower()]


@app.route('/concerts')
def concerts():
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    concert_events = db.session.query(ShowEvent, Event, EventCategory, Place, MetroStations).join(Event).join(EventCategory).\
        join(Place).join(MetroStations).filter(EventCategory.category == "Концерт").all()

    metro_stations_list = db.session.query(MetroStations).all()

    for element in metro_stations_list:
        print(element.name)

    for element in concert_events:
        print(element.Event.name)
        print(element.ShowEvent.date_start)

    #if calendar:
        #concert_events = get_filtered_concers_by_date(calendar)
    return render_template("concert.html", data=concert_events, metro_stations_list=metro_stations_list)





























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

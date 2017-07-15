# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from . import db
from . import create_app
from app.server.database_models import ShowEvent, Event, EventCategory

app = create_app('default')


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
    calendar = request.args.get('calendar')
    concert_events = db.session.query(ShowEvent, Event, EventCategory).join(Event).join(EventCategory).\
        filter(EventCategory.category == "Концерт").all()

    for element in concert_events:
        print(element.Event.name)
        print(element.ShowEvent.date_start)

    #if calendar:
        #concert_events = get_filtered_concers_by_date(calendar)
    return render_template("concert.html", data=concert_events)


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

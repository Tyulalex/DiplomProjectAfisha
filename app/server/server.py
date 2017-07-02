from flask import Flask, render_template, request

app = Flask(__name__)

raw_events = [
    {
        'city': 'moscow',
        'title': 'Премия МУЗтв',
        'date': {
            'from': "12/12/2017",
            'to': "13/12/2017",
        },
        'category': 'concert',
        'location': {
            'latitude': 55.31122,
            'longitude': 52.52121,
            'address': 'ул Горбушкина, 35',
        },
        'price_rub': {
            'from': 1000,
            'to': 15000,
        },
        'age_category': '12+',
        'description': '...',
        'rating': 3,  # 1...10
        'url': "http://..."
    },
    {
        'city': 'saint-petersburg',
        'title': 'Выставка',
        'date': {
            'from': "11/11/2017",
            'to': "21/11/2017",
        },
        'category': 'exhibition',
        'location': {
            'latitude': 55.31122,
            'longitude': 52.52121,
            'address': 'проспект Невского, 5',
        },
        'price_rub': {
            'from': 500,
            'to': 1500,
        },
        'age_category': '6+',
        'description': '...',
        'rating': 4,  # 1...10
        'url': "http://..."
    }
]


@app.route('/')
def main_page():
    events = raw_events
    city = request.args.get('city')
    category = request.args.get('category')
    if city:
        events = get_filtered_data_by_city(events, city)
    if category:
        events = get_filtered_data_by_category(events, category)
    return render_template("index.html", data=events)


def get_filtered_data_by_category(raw_events, category):
    return [event for event in raw_events if event.get('category', '').lower() == category]


def get_filtered_data_by_city(raw_events, city):
    return [event for event in raw_events if event.get('city', '').lower() == city.lower()]


@app.route('/concerts')
def concerts():
    return render_template("index.html", data=get_filtered_data_by_category(raw_events, 'concert'))


@app.route('/movies')
def cinema():
    return render_template("index.html", data=get_filtered_data_by_category(raw_events, 'movies'))


@app.route('/theatres')
def theatres():
    return render_template("index.html", data=get_filtered_data_by_category(raw_events, 'theatres'))


@app.route('/exhibition')
def exhibition():
    return render_template("index.html", data=get_filtered_data_by_category(raw_events, 'exhibition'))

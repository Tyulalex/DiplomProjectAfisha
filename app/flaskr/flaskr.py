from flask import Flask, render_template, request

app = Flask(__name__)

raw_data = [
    {
        'city': 'Москва',
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
        'city': 'Санкт-Петербург',
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
    data = raw_data
    city = request.args.get('city')
    category = request.args.get('category')
    if city:
        data = [element for element in data if element.get('city').lower() == city.lower()]
    if category:
        data = [element for element in data if element.get('category').lower() == category.lower()]
    return render_template("main_page.html", data=data)


@app.route('/concerts')
def display_concerts():
    data = raw_data
    data = [element for element in data if element.get('category').lower() == 'concert']
    return render_template("main_page.html", data=data)
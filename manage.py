from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy.orm import relationship
from sqlalchemy import func
from app.server.server import app


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


#  movie,    play, exhibition,      concert
# cinema, theatre, exhibition area, concert areas

class PlaceType(db.Model):
    __tablename__ = 'place_type'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String()) # cinema, theatre, exhibition area, concert areas
    created_at = db.Column(db.DateTime, default=func.now())


class Place(db.Model):
    __tablename__ = 'place'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(250))
    station_id = db.Column(db.Integer)
    place_type_id = db.Column(db.Integer, db.ForeignKey('place_type.id'))
    created_at = db.Column(db.DateTime, default=func.now())

    place_type = relationship("PlaceType", backref="place")
    station = relationship("MetroStation", backref="place")


class EventCategory(db.Model):
    __tablename__ = 'event_category'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False) #  movie,    play, exhibition,      concert
    created_at = db.Column(db.DateTime, default=func.now())

    def __repr__(self):
        return '<Event type %r>' % (self.category)


class AgeCategory(db.Model):
    __tablename__ = 'age_category'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    def __repr__(self):
        return '<Age category %r>' % (self.category)


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text)
    rating = db.Column(db.String(10))
    age_category_id = db.Column(db.Integer, db.ForeignKey('age_category.id'))
    event_category_id = db.Column(db.Integer, db.ForeignKey('event_category.id'))
    created_at = db.Column(db.DateTime, default=func.now())

    event_category = relationship("EventCategory", backref="event")
    age_category = relationship("AgeCategory", backref="event")


class MetroStation(db.Model):
    __tablename__ = 'station'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))


class EventShow(db.Model):
    __tablename__ = 'event_show'
    id = db.Column(db.Integer, primary_key=True)
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)
    price_from = db.Column(db.Integer)
    price_to = db.Column(db.Integer)
    currency = db.Column(db.String, default = 'RUB')
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    created_at = db.Column(db.DateTime, default=func.now())

    event = relationship("Event", backref="event_show")
    place = relationship("Place", backref="event_show")


if __name__ == '__main__':
    manager.run()
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy.orm import relationship
from app.flaskr.flaskr import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class CategoriesPerEvent(db.Model):
    __tablename__ = 'event_categories'
    id = db.Column(db.Integer, primary_key=True)
    event_category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Event category %r>' % (self.event_category)


class CategoriesPerAge(db.Model):
    __tablename__ = 'age_categories'
    id = db.Column(db.Integer, primary_key=True)
    age_category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Age category %r>' % (self.age_category)


class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text)
    event_category_id = db.Column(db.Integer, db.ForeignKey('event_categories.id'))
    age_category_id = db.Column(db.Integer, db.ForeignKey('age_categories.id'))
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)
    price_min = db.Column(db.DateTime)
    price_max = db.Column(db.DateTime)
    rating = db.Column(db.String(10))
    url = db.Column(db.String(150))
    created_at = db.Column(db.DateTime)

    event_category = relationship("CategoriesPerEvent", backref="events")
    age_category = relationship("CategoriesPerAge", backref="events")

    def __repr__(self):
        return '<Event %r>' % (self.name)


class Cinemas(db.Model):
    __tablename__ = 'cinemas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(250))


class MoviesCinemasMap(db.Model):
    __tablename__ = 'movies_cinemas_map'
    __table_args__ = (
        db.PrimaryKeyConstraint('movie_id', 'cinema_id'),
    )
    movie_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    cinema_id = db.Column(db.Integer, db.ForeignKey('cinemas.id'))


if __name__ == '__main__':
    manager.run()
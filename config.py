import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join('sqlite:///', basedir, 'app.db'))

    @staticmethod
    def init_app(app):
        app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI


config = {
    'default': Config
}
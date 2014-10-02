from flask import Flask

#import flask extensions
from flask.ext.sqlalchemy import SQLAlchemy

#config values
SQLALCHEMY_DATABASE_URI ='sqlite:///example.db'
DEBUG = True
SECRET_KEY = 'development key'

def create_app():
    app = Flask(__name__)
    return app

def config_app(app):
    app.config.from_object(__name__)

app = create_app()
config_app(app)
db = SQLAlchemy(app)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()

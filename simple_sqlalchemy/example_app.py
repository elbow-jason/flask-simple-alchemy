from flask import Flask

#import flask extensions
from flask.ext.sqlalchemy import SQLAlchemy

import config

def create_app():
    app = Flask(__name__)
    return app

def config_app(app, config_obj):
    app.config.from_object(config_obj)


app = create_app()
config_app(app, config)
db = SQLAlchemy(app)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()

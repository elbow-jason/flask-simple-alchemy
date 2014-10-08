from flask import Flask, redirect

from datetime import datetime
from datetime import date

#import flask extensions
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager

from flask_simple_alchemy import Relator

import config


def create_app():
    app = Flask(__name__)
    return app


def config_app(app, config_obj):
    app.config.from_object(config_obj)


app = create_app()
config_app(app, config)

db = SQLAlchemy(app)
manager = APIManager(app, flask_sqlalchemy_db=db)
this_table = Relator(db)

this_table.add('Person')
this_table.add('Computer')
this_table.add('Cat')


@app.route('/')
def to_person():
    return redirect('/api/person')


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    birth_date = db.Column(db.Date)


class Computer(db.Model, this_table.HasManyToOneWith.Person):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    vendor = db.Column(db.String)
    purchase_time = db.Column(db.DateTime)


class Cat(db.Model, this_table.HasOneToOneWith.Person):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    age = db.Column(db.Integer)
    message = db.Column(db.String)

def reset_db():
    db.drop_all()
    db.create_all()


def add_api_endpoints():
    methods = ['GET', 'PUT', 'POST', 'DELETE']
    manager.create_api(Person, methods=methods)
    manager.create_api(Computer, methods=methods)
    manager.create_api(Cat, methods=methods)


def seed_db():
    try:
        p = Person()
        p.name = u"Jason"
        p.birth_date = date.today()
        db.session.add(p)
        db.session.commit()

        computer1 = Computer()
        computer1.name = "elbow"
        computer1.vendor = "ASUS"
        computer1.purchase_time = datetime.utcnow()
        computer1.person = p
        db.session.add(computer1)
        db.session.commit()

        computer2 = Computer()
        computer2.name = "jasons-desktop"
        computer2.vendor = "self-built"
        computer2.purchase_time = datetime.utcnow()
        computer2.person = p
        db.session.add(computer2)
        db.session.commit()

        cat1 = Cat()
        cat1.name = "Ruby"
        cat1.age = 0
        cat1.person = p
        cat1.message = "Ruby will be clobbered by wildman for the database"+\
            " Person.cat relationship since it is a one_to_one"
        db.session.add(cat1)
        db.session.commit()

        cat2 = Cat()
        cat2.name = "Wildman"
        cat2.age = 0
        cat2.message = "Notice that there is no 'Ruby' cat. She was"+\
            " clobbered when Wildman was committed. Notice also that"+\
            " Person.cat is a single dict/json object not a list/array."
        cat2.person = p
        db.session.add(cat2)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise e

if __name__ == '__main__':
    reset_db()
    add_api_endpoints()
    seed_db()
    app.run()

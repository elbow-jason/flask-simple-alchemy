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
    #owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    #owner = db.relationship('Person', backref=db.backref('computers',
    #                                                     lazy='dynamic'))


class Cat(db.Model, this_table.HasOneToOneWith.Person):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    age = db.Column(db.Integer)


def reset_db():
    db.drop_all()
    db.create_all()


def add_api_endpoints():
    methods = ['GET', 'PUT', 'POST', 'DELETE']
    manager.create_api(Person, methods=methods)
    manager.create_api(Computer, methods=methods)
    manager.create_api(Cat, methods=methods)


def seed_db():
    p = Person()
    p.name = u"Jason"
    p.birth_date = date.today()

    nc = Computer()
    nc.name = "elbow"
    nc.vendor = "ASUS"
    nc.purchase_time = datetime.utcnow()
    nc.person = p


    anc = Computer()
    anc.name = "comp1"
    anc.vendor = "ASUS"
    anc.purchase_time = datetime.utcnow()
    anc.person = p


    cat = Cat()
    cat.name = "Ruby"
    cat.age = 0
    cat.person = p


    cat2 = Cat()
    cat2.name = "Wildman"
    cat2.age = 0
    cat2.person = p


    db.session.add(p)
    db.session.add(nc)
    #db.session.add(anc)
    db.session.add(cat)
    #db.session.add(cat2)
    db.session.commit()

    sp = Person.query.first()
    sc = Computer.query.first()

    print sp.__dict__.keys()
    print sc.__dict__.keys()


if __name__ == '__main__':
    reset_db()
    add_api_endpoints()
    seed_db()
    app.run()
